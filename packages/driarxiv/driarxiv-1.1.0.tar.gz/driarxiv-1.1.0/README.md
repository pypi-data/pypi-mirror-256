# driarxiv

![img.png](img.png)

`driarxiv` is a CLI tool designed to transform arXiv papers into comprehensive wikis. It automates the extraction of 
information from specified arXiv papers and their references, creating an organized documentation structure. 
This tool also supports generating documentation from previously created Dria Indexes by inputting 
their contract IDs.

`driarxiv` generates multiple markdown files, where README.md is the main markdown file that contains the summary of the 
paper with multiple links to other markdown files that contain the extracted information from the paper and its references.

The generated wikis are stored in markdown format and can be directly opened as a vault in Obsidian.
![img_1.png](img_1.png)

## How does it work?

`driarxiv` uses the OpenAI API to generate a summary of the paper and then uses the Dria API to extract information from the references. 
The extracted information is then organized into a comprehensive wiki.

1. Download the paper from arXiv.
2. Extract references from the paper.
3. Download the references from arXiv.
4. Create single RAG from the paper and its references.
5. Use GPT to generate a summary of the paper.
6. Ask questions related to paper, use RAG to answer them.
7. GPT strictly uses RAG and prompts "I don't know" if it can't find the answer.
8. Extract named entities and create readmes for each of them.
9. Link entities to the main readme.

## Why Dria?

Briefly:
- It handles both embedding and index for you.
- It's free.
- It creates a public RAG Index, allowing reusability of RAG models.
- Help Dria community to create public knowledge available for AIs.

Just hop on to [dria.co](https://dria.co/) and sign up to get your API key. If you run out of credits
you can get more by filling out a simple form. Credits are to control the usage of API since 
creating a public RAG models requires compute and storage. 

## Prerequisites

Before you can use `driarxiv`, you need to set up your environment with the necessary API keys:

- **OPENAI_API_KEY**: Used for accessing OpenAI's APIs.
- **DRIA_API_KEY**: Required for interacting with Dria's services.

You can set these variables in your environment as follows:

```bash
export OPENAI_API_KEY=your_openai_api_key_here
export DRIA_API_KEY=your_dria_api_key_here
```

Replace your_openai_api_key_here and your_dria_api_key_here with your actual API keys.

## Installation
To install driarxiv, run the following command:
```bash
pip install driarxiv
```

Ensure you have Python 3.9 or later installed.

## Usage

### Generating a Wiki from an arXiv Paper
To generate a comprehensive wiki from an arXiv paper, use:
```bash
driarxiv generate [arxiv_url]
```

Replace [arxiv_url] with the actual URL of the arXiv paper you want to process.


### Using an Existing Dria Index to generate wiki
If someone already created a Dria Index for the paper, you can use the contract ID to generate a wiki:
![dria.png](dria.png)

```bash
```bash
driarxiv from_rag [arxiv_url] [contract_id]
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

