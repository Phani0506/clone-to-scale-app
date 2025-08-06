import os
from llama_index.core import SimpleDirectoryReader
from llama_index.readers.web import BeautifulSoupWebReader

def load_from_directory(path):
    """Loads all documents from a local directory, handling empty directories."""
    print(f"Attempting to load documents from local path: {path}")
    if not os.path.isdir(path) or not os.listdir(path):
        print(f"Directory '{path}' is empty or does not exist. Skipping.")
        return []
    
    loader = SimpleDirectoryReader(path)
    return loader.load_data()

def load_from_urls(urls):
    """Scrapes and loads documents from a list of URLs."""
    print(f"Scraping {len(urls)} URL(s)...")
    loader = BeautifulSoupWebReader()
    return loader.load_data(urls=urls)
