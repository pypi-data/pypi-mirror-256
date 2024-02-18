import arxiv
from tqdm import tqdm
from driarxiv.parser import PDFWorker
from openai import OpenAI
from oaib import Auto
from dria import Dria, Models
from driarxiv.logger_config import logger

import os


class OpenAIWorker:
    def __init__(self):
        self.client = OpenAI()
        self.batch = Auto(workers=8)

    async def get_titles(self, references):
        for ref in references:
            prompt = 'Return the paper title from given passage. ' \
                     'Only prompt the title without any other info including writer names. Passage:{}'.format(
                ref)
            await self.batch.add(
                "chat.completions.create",
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
        results = await self.batch.run()
        results = results.get("result")
        titles = [response["choices"][0]["message"]["content"].replace('"',"").strip() for response in results]
        return titles


class ArxivWorker:
    def __init__(self, tag):
        self.client = arxiv.Client()
        self.dir_path = tag + "/references"

    def _get_downloaded_files(self):
        return os.listdir(self.dir_path)

    def download_file(self, paper):
        files = self._get_downloaded_files()
        fname = "{}.pdf".format(paper.title)
        if fname not in files:
            paper.download_pdf(filename=fname, dirpath=self.dir_path)

    def get_paper_from_url(self, url: str, download: bool = False):
        id = url.split("/")[-1].replace(".pdf", "")
        if "." not in id:
            id = url.split("/")[-2] + "/" + id
        search = arxiv.Search(id_list=[id], max_results=1)
        results = self.client.results(search)
        papers = list(results)
        paper = papers[0]
        if download:
            self.download_file(paper)
        return paper

    def search_for_paper(self, title: str, get_first: bool = True):
        search = arxiv.Search(
            query='ti:"{}"'.format(title),
            max_results=10,
            sort_by=arxiv.SortCriterion.SubmittedDate
        )
        results = self.client.results(search)
        papers = list(results)
        if len(papers) == 0:
            return None
        if get_first:
            return [papers[0]]
        return papers


class DriaArxiv:
    def __init__(self, dria_api_key, tag:str):
        self.pdf_worker = PDFWorker()
        self.tag = tag
        self.opeanai_worker = OpenAIWorker()
        self.arxiv_worker = ArxivWorker(tag)
        self.dria_index = Dria(api_key=dria_api_key)

    @staticmethod
    def filename(paper):
        return "{}.pdf".format(paper.title)

    def get_chunks_and_references(self, fname):
        return self.pdf_worker.from_file(fname, self.tag)

    async def create_files_and_chunks(self, paper, depth=1):
        if depth > 3:
            raise ValueError("Depth cannot be more than 3")

        logger.info("Creating files and chunks for paper: {}".format(paper.title))
        data = []
        worked_on = []
        original_chunks, original_references = self.get_chunks_and_references(self.filename(paper))

        paper_titles = await self.opeanai_worker.get_titles(original_references)

        logger.info("Adding origin paper's chunks: %s\n", paper.title)

        for chunk in tqdm(original_chunks):
            data.append({"text": chunk, "metadata": {"text": chunk, "title": paper.title}})

        worked_on.append(paper.title)

        d = 0
        while d < depth:
            new_refs = []
            logger.info("Working on references...")
            for title in tqdm(paper_titles):
                _p = self.arxiv_worker.search_for_paper(title)
                if _p is None:
                    continue
                _p = _p[0]

                try:
                    self.arxiv_worker.download_file(_p)
                except:
                    try:
                        self.arxiv_worker.download_file(_p)
                    except:
                        continue

                if _p.title in worked_on:
                    continue
                else:
                    chunks_, refs_ = self.get_chunks_and_references(self.filename(_p))

                    for chunk in chunks_:
                        data.append({"text": chunk, "metadata": {"text": chunk, "title":_p.title}})

                    worked_on.append(_p.title)

                    if d+1 < depth:
                        paper_titles = await self.opeanai_worker.get_titles(refs_)
                        new_refs += paper_titles

            paper_titles = list(set(new_refs))
            d += 1

        return data

    async def create_wiki(self, url):

        def chunked_list(data, n):
            for i in range(0, len(data), n):
                yield data[i:i + n]

        paper = self.arxiv_worker.get_paper_from_url(url, download=True)
        data = await self.create_files_and_chunks(paper)

        contract_id = self.dria_index.create(
            name=paper.title,
            embedding=Models.bge_base_en,
            category=paper.primary_category,
            description=paper.summary)

        for batch in tqdm(chunked_list(data, 1000), desc="Inserting chunks into index"):
            _ = self.dria_index.insert_text(
                batch
            )

        return contract_id
