from typing import List
import xml.etree.ElementTree as ET
from backend.data_parsers.pedo_chat_structure import Message, Conversation, Person, People
from backend.utils.debug_mode import debug
from backend.utils.log_mode import set_log_mode
set_log_mode('test')

import json
import os


def get_pedo_account_ids() -> set[str]:
    file_path = '././unzipped-data/raw-pedo-chat-data/Training-Data/pan12-sexual-predator-identification-training-corpus-predators-2012-05-01.txt'
    with open(file_path, 'r') as file:
        return set(line.strip() for line in file)

def save_object_to_json(obj, filename):
    with open(filename, 'w') as file:
        json.dump(obj, file, indent=4)

# def parse_xml_and_save(xml_file: str):
#     people, convos = parse_xml(xml_file)
#      # Save People objects
#     for person in people:
#         filename = f'././unzipped-data/parsed-pedo-chat-data/new-people/{person.id}.json'
#         os.makedirs(os.path.dirname(filename), exist_ok=True)
#         save_object_to_json(person.to_dict(), filename)
#     # Save Conversation objects
#     for convo in convos:
#         filename = f'.././unzipped-data/parsed-pedo-chat-data/new-conversations/{convo.id}.json'
#         os.makedirs(os.path.dirname(filename), exist_ok=True)
#         save_object_to_json(convo.to_dict(), filename)
#     people_files = os.listdir('././unzipped-data/parsed-pedo-chat-data/new-people')
#     convo_files = os.listdir('././unzipped-data/parsed-pedo-chat-data/new-conversations')
#     print("Saved People files:", people_files)
#     print("Saved Conversation files:", convo_files)

def parse_xml_and_save_optimized(xml_file: str = [], should_save:bool = False) -> None:
    debug("START", mode='test')
    # print("START")
    PEOPLE = set()
    CONVOS = []
    convo_ids = set()
    tree = ET.parse(xml_file)
    root = tree.getroot()
    pedo_ids = get_pedo_account_ids()


    for conv in root.findall('conversation'):
        debug("Checking conversation", mode='test')
        conv_id = conv.get('id')
        debug(conv_id)
        messages = []
        person_ids = []
        temp_messages = conv.findall('message')
        if len(temp_messages) < 40:
            continue
        
        for msg in temp_messages:
            line_num = int(msg.get('line'))
            author_id = msg.find('author').text
            timestamp = msg.find('time').text
            content = msg.find('text').text
            debug(line_num, author_id, timestamp, content, mode='debug_BRUH')
            message = Message(line_num, author_id, timestamp, content)
            messages.append(message)
            
            if author_id not in person_ids:
                person_ids.append(author_id)
                PEOPLE.add(author_id)
            else: debug("Person already exists")
        
            
        convo_exists = conv_id in convo_ids
        if not convo_exists:
            debug("Creating new conversation", conv_id, person_ids)
            conversation = Conversation(conv_id, messages, person_ids)
            debug("Created new conversation - ", conversation.id, conversation.person_ids)
            CONVOS.append(conversation)
            convo_ids.add(conv_id)
            if should_save:
                filename = f'././unzipped-data/parsed-pedo-chat-data/new-conversations/{conversation.id}.json'
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                save_object_to_json(conversation.to_dict(), filename)
            print("Created convo #: ", len(CONVOS))
        else:
            ValueError("Conversation already exists")
        # debug("Checking if we should break", mode='test')
        # if len(CONVOS) > 2:
        #     debug(CONVOS, mode='test')
        #     debug(len(CONVOS), mode='test')
        #     debug(PEOPLE, mode='test')
        #     break
    
    people_dict = {}
    for person_id in PEOPLE:
        people_dict[person_id] = {"id": person_id, "conversation_ids": set(), "is_pedo": person_id in pedo_ids}
    for convo in CONVOS:
        for person_id in convo.person_ids:
            people_dict[person_id]["conversation_ids"].add(convo.id)
    for person_id in people_dict:
        people_dict[person_id]["conversation_ids"] = list(people_dict[person_id]["conversation_ids"])
        if should_save:
            filename = f'././unzipped-data/parsed-pedo-chat-data/new-people/{person_id}.json'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            save_object_to_json(people_dict[person_id], filename)
    people_files = os.listdir('././unzipped-data/parsed-pedo-chat-data/new-people')
    convo_files = os.listdir('././unzipped-data/parsed-pedo-chat-data/new-conversations')
    print("Saved People files:", people_files)
    print("Saved Conversation files:", convo_files)
    debug("END")
    return


# def parse_xml(xml_file: str) -> List[Person]:
#     debug("START")
#     print("START")
#     PEOPLE = People([], set())
#     CONVOS = []
#     tree = ET.parse(xml_file)
#     root = tree.getroot()
#     pedo_ids = get_pedo_account_ids()
#     for conv in root.findall('conversation'):
#         conv_id = conv.get('id')
#         debug(conv_id)
#         messages = []
#         person_ids = []  
#         for msg in conv.findall('message'):
#             line_num = int(msg.get('line'))
#             author_id = msg.find('author').text
#             timestamp = msg.find('time').text
#             content = msg.find('text').text
#             debug(line_num, author_id, timestamp, content)
#             message = Message(line_num, author_id, timestamp, content)
#             messages.append(message)
#             person = PEOPLE.get_person_by_id(author_id)
#             if person is None:
#                 debug("Creating new person", author_id)
#                 is_pedo = author_id in pedo_ids
#                 person = Person(author_id, set(), is_pedo)
#                 PEOPLE.add_person(person)
#             if author_id not in person_ids:
#                 person_ids.append(author_id)
#             else: debug("Person already exists")
#         has_conversation = PEOPLE.has_conversation_id(conv_id)
#         if not has_conversation:
#             conversation = Conversation(conv_id, messages, person_ids)
#             CONVOS.append(conversation)
#             print("Created convo #: ", len(CONVOS))
#             debug("Created new conversation - ", conversation)
#             debug(conversation)
#             for person_id in person_ids:
#                 person = PEOPLE.get_person_by_id(person_id)
#                 person.add_conversation_id(conv_id)
#         else:
#             ValueError("Conversation already exists")
#         if len(CONVOS) > 10:
#             return PEOPLE.people, CONVOS
#     debug("END")
#     return PEOPLE.people, CONVOS


parse_xml_and_save_optimized('././unzipped-data/raw-pedo-chat-data/Training-Data/pan12-sexual-predator-identification-training-corpus-2012-05-01.xml', should_save=True)

