import re
from abc import ABC, abstractmethod
from io import BytesIO

import json


class FileWorker(ABC):

    @abstractmethod
    def to_chunks(self, fname):
        pass

    @staticmethod
    def chunk_list(lst, chunk_size):
        """Yield successive chunk_size chunks from lst."""
        for i in range(0, len(lst), chunk_size):
            yield lst[i:i + chunk_size]

    @staticmethod
    def read_response_bytes(response):
        stream = BytesIO()
        for chunk in response.iter_content(chunk_size=1024 * 1024):  # Process the stream in chunks of 1MB
            stream.write(chunk)
        stream.seek(0)

        return stream

    @staticmethod
    def remove_references(text):
        import re
        cleaned = re.sub(r'\[\d+\]', '', text)
        cleaned = ' '.join(cleaned.split())
        return cleaned

    def clean_text(self, text):
        if text == "":
            return text
        text = text.replace('- ', '').replace('\n', ' ')
        text = text.replace('/*', '').replace('*/', '').replace('@', '')
        text = text.replace('w/', 'with ')
        text = ' '.join(text.split())
        text = self.remove_references(text)
        text = self.remove_urls(text)
        if len(text) == 0:
            return ""
        if text[0].islower():
            try:
                text = self.split_after_first_char_regex(text, ['.', '?', '!', "'"])
            except Exception as e:
                return text
        return text

    @staticmethod
    def remove_urls(text):
        return re.sub(r'http[s]?://\S+', '', text)

    @staticmethod
    def split_after_first_char_regex(text, char_list):
        pattern = '[' + re.escape(''.join(char_list)) + ']'
        match = re.search(pattern, text)

        if match:
            position = match.end()
            return text[position:]
        else:
            return ''


