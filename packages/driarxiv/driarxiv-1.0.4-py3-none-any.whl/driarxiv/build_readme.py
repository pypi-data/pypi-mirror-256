from dria import Dria
from openai import OpenAI
from driarxiv.worker import ArxivWorker
from driarxiv.parser import PDFWorker
import re
import tiktoken
from time import time
from tqdm import tqdm
import os
from driarxiv.logger_config import logger


def filename_from_title(title):
    return title.lower().replace(" ", "_").replace(":", "").\
        replace("?", "").replace("!", "").replace("(", "").\
        replace(")", "").replace("/", "").replace("\\", "").\
        replace("'", "").replace('"', "").replace("*", "").replace(".", "")

def replace_term_with_link(text, term, fname):
    escaped_term = re.escape(term)
    replacement = r'[\g<0>](docs/{}.md)'.format(fname.lower())
    result = re.sub(r'\b' + escaped_term + r'\b', replacement, text)

    return result


def replace_term_with_link_in_docs(text, term, fname):
    escaped_term = re.escape(term)
    replacement = r'[\g<0>]({}.md)'.format(fname.lower())
    result = re.sub(r'\b' + escaped_term + r'\b', replacement, text)

    return result


def get_context(question, dria_client, encoder):
    ctx = dria_client.search(question, top_n=20, rerank=True, level=0)
    ctx = " ".join([c["metadata"] for c in ctx if c["score"] > 0.8])
    ctx = encoder.decode(encoder.encode(ctx)[:8130])
    return ctx


class OpenAIWorker:
    def __init__(self):
        self.client = OpenAI()
        self.messages = [{"role": "system", "content": "You are a helpful assistant."}]

    def hard_reset(self):
        self.messages = [{"role": "system", "content": "You are a helpful assistant."}]

    def ask_gpt(self, question, context):
        p = """Use the following pieces of context to answer the user question. This context retrieved from a knowledge base and you should use only the facts from the context to answer.
        Your answer must be based on the context. If the context not contain the answer, just say that 'I don't know', don't try to make up an answer, use the context.
        Don't address the context directly, but use it to answer the user question like it's your own knowledge.
        
        While answering, use technical language and be concise. Add '$' around latex math equations.

        Context:
        """
        p += context
        p += "\n"
        p += "Question: {}".format(question)

        self.messages.append({"role": "user", "content": p})
        response = self.client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=self.messages)

        self.messages.append({"role": "system", "content": response.choices[0].message.content})

        return response.choices[0].message.content

    def ner(self, readme):

        response = self.client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Return the named entities from given passage the way they are written inside the text."
                                            "Directly write them without letters, number or bulletpoints, write them line by line. "
                                            "If two entities are same but written differently (like abbravations) write only one of them." 
                                            "For instance write 'United States' and 'USA' as 'United States' instead of two lines."
                                            "For instance write 'John Coltrane's and 'John Coltrane' as 'John Coltrane' instead of two lines."
                                            "For instance write 'Large Language Model' and 'LLMs' as 'Large Language Model' instead of two lines."
                                            "Seperate them by '\n' Passage:{}".format(readme)
                 },
            ]
        )
        self.messages.append({"role": "system", "content": response.choices[0].message.content})

        return response.choices[0].message.content


def run(url, contract_id, tag):
    st = time()
    # Create dir
    encoder = tiktoken.encoding_for_model("gpt-4")
    da = Dria(api_key=os.environ["DRIA_API_KEY"])
    da.set_contract(contract_id)
    arxiv_worker = ArxivWorker(tag)
    pdfworker = PDFWorker()
    oaw = OpenAIWorker()

    readmes = {}
    readmes["main"] = []

    paper = arxiv_worker.get_paper_from_url(url, download=True)
    fname = "{}.pdf".format(paper.title)

    # First ask what is the paper about
    logger.info("Asking gpt what the paper is about.")
    question = "What is {}? Write a comprehensive answer".format(paper.title)
    context = get_context(question, da, encoder)
    response = oaw.ask_gpt(question, context)
    readmes["main"].append(response)

    # Ask about the methodology outline
    logger.info("Asking gpt about the methodologies of the paper.")
    question = "List the methodology of {}, outline processes and explain step by step. Use technical language, but make it concise".format(paper.title)
    sub_q = "What is the methodology of {}?".format(paper.title)
    context = get_context(sub_q, da, encoder)
    response = oaw.ask_gpt(question, context)
    readmes["main"].append(response)

    logger.info("Asking gpt about the results and benchmarks")
    question = "What are the results and benchmarks of {}?. Make it concise".format(paper.title)
    context = da.search(question, top_n=20, rerank=False, level=0)
    context = " ".join([c["metadata"]["text"] for c in context if c["score"] > 0.65 and c["metadata"]["title"] == paper.title])
    context = encoder.decode(encoder.encode(context)[:8191 - len(encoder.encode(question))])
    response = oaw.ask_gpt(question, context)
    readmes["main"].append(response)
    oaw.hard_reset()

    # Ask gpt to create questions about paper
    logger.info("Asking gpt to create fundamental questions about the paper")
    question = "Create a list of fundamental questions you think needs to be explored for given context to be understood. No more than 3 questions. Only ask questions if you think the are neccessary for understanding the underyling mechanisms. If the question you asked is already answered within context, dont ask it. Seperate questions by a new line."
    context = " ".join(readmes["main"])
    context = encoder.decode(encoder.encode(context)[:8130])
    response = oaw.ask_gpt(question, context)
    qs = response.split("\n")
    qs = [q for q in qs if len(q) > 7]

    logger.info("GPT answering the questions")
    for question in qs:
        context = get_context(question, da, encoder)
        response = oaw.ask_gpt(question, context)
        readmes["main"].append(question)
        readmes["main"].append(response)
        oaw.hard_reset()


    master_readme = "\n".join(readmes["main"])
    named_entities = oaw.ner(master_readme)
    named_entities = list(set(named_entities.split("\n")))
    logger.info("Creating readmes for named entities")
    for entity in tqdm(named_entities):
        question = "How {} is related to {}? Explain profoundly, with technical details".format(entity, paper.title)
        context = get_context(entity, da, encoder)
        if context == "":
            continue
        readmes[entity] = []
        response = oaw.ask_gpt(question, context)
        readmes[entity].append(response)
        oaw.hard_reset()

    logger.info("Writing readmes to disk")
    all_readmes = {k: "\n".join(v) for k,v in readmes.items() if k != "main"}
    all_readmes = {k:v for k,v in all_readmes.items() if "I don't know" not in v}

    for k, v in all_readmes.items():

        ks = set(all_readmes.keys())
        ks.remove(k)
        for key in ks:
            fname = filename_from_title(key)#key.lower().replace(" ", "_")
            v = replace_term_with_link_in_docs(v, key, fname)

        fname = filename_from_title(k) #k.lower().replace(" ", "_")
        with open(tag + "/docs/{}.md".format(fname), "w") as f:
            f.write("{}".format(v))
        master_readme = replace_term_with_link(master_readme, k, fname)

    with open(tag + "/README.md".format(tag), "w") as f:
        f.write(master_readme)

    logger.info("Done in {} seconds".format(time()-st))



if __name__ == "__main__":
    run("https://arxiv.org/pdf/2310.11454.pdf", "gl5XQxrYWrqS4xgak24W1vy8ORGilOBHPU_K2CjVfmo")