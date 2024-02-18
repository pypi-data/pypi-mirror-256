from setuptools import setup, find_packages

setup(
    name='investment_functions',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pinecone-client',
        'langchain',
        'PyPDF2',
        'docx2txt',
        'openai',
        'sentence-transformers',
        'nltk',
        'config'
    ],
    entry_points={
        'console_scripts': [
            # Add any console scripts here if applicable
        ],
    },
)