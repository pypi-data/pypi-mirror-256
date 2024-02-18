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
asdsa

## Why Dria?


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




## License
This project is licensed under the MIT License - see the LICENSE file for details.

