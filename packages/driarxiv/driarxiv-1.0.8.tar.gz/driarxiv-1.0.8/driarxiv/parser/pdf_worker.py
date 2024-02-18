from abc import ABC

from driarxiv.parser.base import FileWorker
import time
from tqdm import tqdm
import requests

class PDFWorker(FileWorker):

    def from_file(self, fname, tag):
        from unstructured.partition.pdf import partition_pdf
        from unstructured.chunking.title import chunk_by_title
        import re
        from unstructured.cleaners.core import clean_non_ascii_chars, clean_extra_whitespace, group_broken_paragraphs, \
            replace_unicode_quotes
        para_split_re = re.compile(r"(\s*\n\s*){3}")

        elements = partition_pdf(filename= tag + "/references/" + fname, include_page_breaks=False, strategy="fast")
        for el in elements:
            el.apply(replace_unicode_quotes)
            el.apply(clean_extra_whitespace)
            el.apply(clean_non_ascii_chars)

        ind = 0
        for i, el in enumerate(elements):
            if "REFERENCES" in el.text or "References" in el.text:
                ind = i
                break

        chunks = chunk_by_title(elements[:ind], max_characters=1000)

        for chunk in chunks:
            chunk.text = group_broken_paragraphs(chunk.text, paragraph_split=para_split_re)
            chunk.text = self.clean_text(chunk.text)

        references = elements[ind:]
        references = [ref.text for ref in references if len(ref.text) > 20]

        return [chunk.text for chunk in chunks if len(chunk.text)>10], references
