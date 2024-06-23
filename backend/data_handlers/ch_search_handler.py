import os
import json
import faiss

from typing import List, Dict
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

from backend.ai_abstractions.ai_models import set_keys
set_keys()

class SimpleDocstore:
    def __init__(self, docs: Dict[int, Document]):
        self.docs = docs

    def search(self, doc_id: int) -> Document:
        return self.docs.get(doc_id)
    
    def get_all_documents(self) -> List[Document]:
        return list(self.docs.values())

def load_faiss_index(index_file: str, metadata_file: str):
    index = faiss.read_index(index_file)
    with open(metadata_file, 'r') as file:
        data = json.load(file)
    documents = [Document(**doc) for doc in data]
    docstore = SimpleDocstore({i: doc for i, doc in enumerate(documents)})
    embedding_function = OpenAIEmbeddings()
    return FAISS(index=index, docstore=docstore, index_to_docstore_id={i: i for i in range(len(documents))}, embedding_function=embedding_function)

def search_episode(episode: int, query: str):
    text_file, index_file, metadata_file, speakers_file = episode_to_filepaths(episode)
    index = load_faiss_index(index_file, metadata_file)
    embedding_function = OpenAIEmbeddings()
    query = str(query)  # Ensure the query is a string
    query_vec = embedding_function.embed_query(query)
    results = index.similarity_search_with_score_by_vector(query_vec, k=3)
    return results

def get_all_chunks(episode: int) -> List[Document]:
    text_file, index_file, metadata_file, speakers_file = episode_to_filepaths(episode)
    index = load_faiss_index(index_file, metadata_file)
    all_documents = index.docstore.get_all_documents()
    return all_documents

def episode_to_filepaths(episode: int) -> List[str]:
    text_file = f'././unzipped-data/chris-hansen-data/Episode-{episode}/Episode-{episode}.txt'
    index_file = f'././unzipped-data/chris-hansen-data/Episode-{episode}/Episode-{episode}.idx'
    metadata_file = f'././unzipped-data/chris-hansen-data/Episode-{episode}/Episode-{episode}.json'
    speakers_file = f'././unzipped-data/chris-hansen-data/Episode-{episode}/Episode-{episode}_speakers.json'
    # Ensure all files exist
    if not all([os.path.exists(file) for file in [text_file, index_file, metadata_file, speakers_file]]):
        raise FileNotFoundError(f"Episode {episode} does not exist")
    return text_file, index_file, metadata_file, speakers_file

# results = search_episode(4, 'Reason for being a pedophile')
# for result in results:
#     print(result)

# print(len(get_all_chunks(4)))