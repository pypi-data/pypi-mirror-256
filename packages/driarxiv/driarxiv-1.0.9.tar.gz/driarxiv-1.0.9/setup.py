from setuptools import setup, find_packages

setup(
    name='driarxiv',
    version='1.0.9',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'driarxiv=driarxiv.run:main',
        ],
    },
    install_requires=[
        'openai>=0.10.2',
        'arxiv>=1.3.0',
        'tqdm>=4.61.2',
        'dria>=0.1.14',
        'unstructured',
        'unstructured[pdf]',
        'oaib==1.0.1',
        'tiktoken'
    ],
    python_requires='>=3.9',
    description='driarxiv: A CLI tool to generate a comprehensive wiki from arXiv papers.',
    author='andthattoo',
    author_email='omer@firstbatch.xyz',
    url='https://github.com/andthattoo/driarxiv',
)