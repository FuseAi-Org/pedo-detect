from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from typing import List
import json
import faiss
from backend.utils.debug_mode import debug
from backend.utils.log_mode import set_log_mode
from backend.ai_abstractions.ai_models import set_keys
import os
set_log_mode('debug')
set_keys()
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=2000,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)


def save_faiss_index(index, index_file: str):
    faiss.write_index(index.index, index_file)

def save_metadata(doc_list: List[Document], metadata_file: str, speaker_file: str) -> None:
    debug("START")
    data_to_store = []
    unique_speaker_ids = set()
    unique_speaker_chunks = {}
    for doc in doc_list:
        metadata = doc.metadata
        data_to_store.append({
            'page_content': doc.page_content,
            'metadata': doc.metadata
        })
        unique_speaker_ids.update(metadata['speaker_ids'])
        for speaker_id in metadata['speaker_ids']:
            if speaker_id not in unique_speaker_chunks:
                unique_speaker_chunks[speaker_id] = set()
            unique_speaker_chunks[speaker_id].add(metadata['chunk_id'])
    formatted_speaker_data = []
    sorted_ids = sorted(list(unique_speaker_ids))
    debug(sorted_ids)
    for speaker_id in sorted_ids:
        formatted_speaker_data.append({
            'speaker_id': speaker_id,
            'chunk_ids': sorted(list(unique_speaker_chunks[speaker_id]))
        })
    with open(metadata_file, 'w') as file:
        json.dump(data_to_store, file, indent=4)
    with open(speaker_file, 'w') as file:
        json.dump(formatted_speaker_data, file, indent=4)
    debug("END")

def get_speaker_ids_and_time(text: str):
    debug("START", mode='debug_deep')
    speaker_ids = set()
    min_time = "99:99:99"
    max_time = "00:00:00"
    debug(text, mode='debug_BRUH')
    text = text.split('\n')
    debug(text, mode='debug_BRUH')
    for i in range(len(text)):
        debug(i, mode='debug_BRUH')
        debug(text[i], mode='debug_BRUH')
        split_info = text[i].split('    ')
        debug(split_info, mode='debug_BRUH')
        spkr = split_info[0]
        time = split_info[1]
        spkr_num = spkr.split(' ')[1]
        speaker_ids.add(int(spkr_num))
        if time < min_time:
            min_time = time
        if time > max_time:
            max_time = time
        debug(text[i], mode='debug_BRUH')
    debug("END", mode='debug_deep')
    return min_time, max_time, list(speaker_ids)


def attach_doc_metadata(doc_list: List[Document],  file_path: str) -> None:
    debug("START", len(doc_list))
    for i in range(len(doc_list)):
        doc = doc_list[i]
        min_time, max_time, speaker_ids = get_speaker_ids_and_time(doc.page_content)
        new_metadata = {"chunk_id": i, "file_path": file_path, "start_time": min_time, "end_time": max_time, "speaker_ids": speaker_ids}
        doc.metadata.update(new_metadata)
    debug("END")
    return

def chunk_and_store(txt_file: str, index_file: str, metadata_file: str, speaker_file: str):
    debug("START")
    with open(txt_file, 'r') as file:
        text = file.read()
    chunks = text_splitter.create_documents([text])
    debug("Chunks created", len(chunks))
    attach_doc_metadata(chunks, txt_file)
    faiss_index = FAISS.from_documents(chunks, OpenAIEmbeddings())
    save_faiss_index(faiss_index, index_file)
    save_metadata(chunks, metadata_file, speaker_file)
    debug("END")


def parse_episodes(reset_mode=False):
    data_path ='././unzipped-data/'
    subdirectories = [d for d in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, d))]
    if 'chris-hansen-data' not in subdirectories:
        debug("No Chris Hansen data found")
        return
    data_path = data_path + 'chris-hansen-data/'
    subdirectories = [d for d in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, d))]
    debug(subdirectories)
    for directory in subdirectories:
        if not directory.startswith('Episode-'):
            debug("Skipping cus not an episode", directory)
            continue
        txt_file = data_path + directory + '/' + directory + '.txt'
        # Ensure the txt file already exist
        if not os.path.exists(txt_file):
            debug("Skipping cus dont have data", txt_file)
            continue
        idx_file = data_path + directory + '/' + directory + '.idx'
        json_file = data_path + directory + '/' + directory + '.json'
        speakers_file = data_path + directory + '/' + directory + '_speakers.json'
        all_files_exist = os.path.exists(idx_file) and os.path.exists(json_file) and os.path.exists(speakers_file)
        if all_files_exist and not reset_mode:
            debug("Skipping cus already processed", idx_file, json_file, speakers_file)
            continue
        chunk_and_store(txt_file, idx_file, json_file, speakers_file)



parse_episodes()
