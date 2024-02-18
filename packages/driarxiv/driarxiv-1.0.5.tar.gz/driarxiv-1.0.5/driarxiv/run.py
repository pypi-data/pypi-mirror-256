import argparse
import os

from driarxiv.worker import DriaArxiv
from driarxiv.build_readme import run
import asyncio
import logging
from driarxiv.logger_config import logger


async def main():

    logging.getLogger('asyncio').setLevel(
        logging.WARNING)  # Remove asyncio debug and info messages, but leave warnings.
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("arxiv").setLevel(logging.WARNING)

    parser = argparse.ArgumentParser(description='Driarxiv a CLI to generate a comprehensive wiki from arXiv papers.')
    subparsers = parser.add_subparsers(dest='command')

    # Add command
    parser_add = subparsers.add_parser('generate', help="Create a docs from paper and it's references.")
    parser_add.add_argument('arxiv_url', type=str, help='URL of the paper')

    # Add command
    parser_add = subparsers.add_parser('from_rag', help="Create a docs from paper and it's references.")
    parser_add.add_argument('arxiv_url', type=str, help='URL of the paper')
    parser_add.add_argument('contract_id', type=str, help='contract_id of dria index')

    args = parser.parse_args()

    if args.command == 'generate':
        url = args.arxiv_url
        tag = url.split("/")[-1].replace(".pdf", "")
        logger.info("Working on %s", tag)
        # Create docs directory if it does not exist
        if not os.path.exists(tag):
            os.makedirs(tag)
        if not os.path.exists(tag + "/docs"):
            os.makedirs(tag + "/docs")

        if not os.path.exists(tag + "/references"):
            os.makedirs(tag + "/references")

        da = DriaArxiv(dria_api_key=os.environ["DRIA_API_KEY"], tag=tag)
        contract_id = await da.create_wiki(url)
        run(url, contract_id, tag)

    elif args.command == 'from_rag':
        url = args.arxiv_url
        tag = url.split("/")[-1].replace(".pdf", "")

        if not os.path.exists(tag):
            os.makedirs(tag)
        if not os.path.exists(tag + "/docs"):
            os.makedirs(tag + "/docs")

        if not os.path.exists(tag + "/references"):
            os.makedirs(tag + "/references")

        url = args.arxiv_url
        contract_id = args.contract_id
        run(url, contract_id, tag)

if __name__ == '__main__':
    asyncio.run(main())
