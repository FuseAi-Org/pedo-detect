import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from backend.ai_abstractions.ai_models import set_keys
from backend.data_handlers.ch_search_handler import load_faiss_index
from backend.utils.log_mode import set_log_mode
from backend.utils.debug_mode import debug
import json
set_log_mode('debug')
set_keys()

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=2000,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)

def chat_handler(chat_history: str, query: str):
    # TODO: Modify index and metadata file chats
    index_file = 3
    metadata_file = 2
    index = load_faiss_index(index_file, metadata_file)
    embedding_function = OpenAIEmbeddings()
    query = str(query)  # Ensure the query is a string
    query_vec = embedding_function.embed_query(query)
    results = index.similarity_search_with_score_by_vector(query_vec, k=3)
    return results

# convert all json files in unzipped-data/chris-hansen-data/parsed-pedo-chat-data/conversations to idx files
def read_json_data():
    data_path ='././unzipped-data/parsed-pedo-chat-data/new-conversations/'

    # subdirectories = [d for d in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, d))]
    # if 'parsed-pedo-chat-data' not in subdirectories:
    #     debug("parsed-pedo-chat-data")
    #     return
    # data_path = data_path + 'parsed-pedo-chat-data'
    files = [f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f))]
    # debug(files)

    # extract id, messages, and person_ids from each json file

    test = files[6]

    with open(data_path + test, 'r') as f:
        data = json.load(f)
        
        id = data['id']
        messages = json.dumps(data['messages'])
        person_ids = data['person_ids']


        docs = [Document(page_content=messages, metadata={'id': id, 'person_ids': person_ids})]

        index = FAISS.from_documents(docs, embedding=OpenAIEmbeddings())
        debug(index)
        debug(index.similarity_search_with_score_by_vector(OpenAIEmbeddings().embed_query("kiss you"), k=3))
        
    # create faiss index and metadata files for each json file
    # meta data will contain id and person_ids
    # faiss index will contain messages


    
    
read_json_data()   