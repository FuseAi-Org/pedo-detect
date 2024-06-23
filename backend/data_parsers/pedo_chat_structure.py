import xml.etree.ElementTree as ET
from typing import List
from backend.utils.debug_mode import debug
from backend.utils.log_mode import set_log_mode
# set_log_mode('all')

class Message():

    def __init__(self, line_num: int, author_id: int, timestamp: str, content: str):
        debug("START")
        self.id = id
        self.line_num = line_num
        self.author_id = author_id
        self.content = content
        self.set_timestamp(timestamp)
        debug("END")

    def set_timestamp(self, timestamp: str):
        debug("START")
        # Validate timestamp format (HH:MM)
        if not isinstance(timestamp, str) or not timestamp.count(':') == 1:
            raise ValueError("Timestamp must be a string in HH:MM format")
        hours, minutes = timestamp.split(':')
        if not (hours.isdigit() and minutes.isdigit() and 0 <= int(hours) < 24 and 0 <= int(minutes) < 60):
            raise ValueError("Invalid time. Hours must be between 00 and 23, and minutes between 00 and 59.")
        self.timestamp = timestamp
        debug("END")
    
    def __str__(self):
        return f"Message {self.line_num} from {self.author_id}: {self.content}"
    
    def chat_format(self):
        return f"{self.author_id} ({self.timestamp}): {self.content}"

class Conversation():
    def __init__(self, id: str, messages:List[Message], person_ids:List[str]):
        debug("START")
        self.id = id
        self.messages = messages
        self.person_ids = person_ids
        debug(self, "END")

    def __str__(self):
        return f"Conversation {self.id} with {len(self.person_ids)} people and {len(self.messages)+1} messages"
    
    def to_dict(self):
        return {
            'id': self.id,
            'messages': [message.chat_format() for message in self.messages],
            'person_ids': self.person_ids
        }
    
    def get_message_by_line(self, line_num: int) -> Message:
        debug("START")
        for message in self.messages:
            if message.line_num == line_num:
                debug(message, "END")
                return message
        debug("END")
        return None
    
    def has_person_id(self, person_id: str) -> bool:
        debug("START")
        for id in self.person_ids:
            if id == person_id:
                debug("END")
                return True
        debug("END")
        return False
    
    
    def add_person_id(self, person_id: str) -> None:
        debug("START")
        if self.has_person_id(person_id):
            raise ValueError("Person ID already in Conversation")
        self.person_ids.append(person_id)
        debug("END")


    def add_message(self, message: Message):
        debug("START")
        old_message = self.get_message_by_line(message.line_num)
        if old_message is not None:
            debug("Message already in Conversation", self, self.messages[0])
            if old_message.author_id == message.author_id and old_message.content == message.content and old_message.timestamp == message.timestamp:
                debug("END")
                return
            raise ValueError("Message line number already in Conversation AND the message is different")
        if message.line_num != len(self.messages) + 1:
            raise ValueError("Message line number must be the next in the sequence")
        self.messages.append(message)
        debug("END")

class Person():
    # def __init__(self, id: str, conversations: List[Conversation]):
    #     debug("START")
    #     self.id = id
    #     self.conversations = conversations
    #     debug("END")
    def __init__(self, id: str, conversation_ids: set[str], is_pedo: bool):
        debug("START")
        self.id = id
        self.conversation_ids = conversation_ids
        self.is_pedo = is_pedo
        debug("END")
    
    def to_dict(self):
        return {
            'id': self.id,
            'conversation_ids': list(self.conversation_ids),
            'is_pedo': self.is_pedo
        }
    
    def __str__(self):
        return f"Person {self.id} with {len(self.conversation_ids)} conversations"
    
    # def has_conversation_id(self, conversation_id: str) -> bool:
    #     debug("START")
    #     for conversation in self.conversations:
    #         if conversation.id == conversation_id:
    #             debug("END")
    #             return True
    #     debug("END")
    #     return False
    def has_conversation_id(self, conversation_id: str) -> bool:
        debug("START")
        has_id = conversation_id in self.conversation_ids
        debug(has_id, "END")
        return has_id
    
    # def add_conversation(self, conversation: Conversation) -> None:
    #     debug("START")
    #     self.conversations.append(conversation)
    #     debug("END")
    def add_conversation_id(self, conversation_id: str) -> None:
        debug("START")
        self.conversation_ids.add(conversation_id)
        debug("END")
    


class People():
    def __init__(self, people: List[Person], conversation_ids: set[str]):
        debug("START")
        self.people = people
        self.conversation_ids = conversation_ids
        debug("END")
    
    def has_person_id(self, person_id: str) -> bool:
        debug("START")
        for person in self.people:
            if person.id == person_id:
                debug("END")
                return True
        debug("END")
        return False
    
    def get_person_by_id(self, person_id: str) -> Person:
        debug("START")
        for person in self.people:
            if person.id == person_id:
                debug("END")
                return person
        debug("END")
        return None
    
    def add_person(self, person: Person) -> None:
        debug("START")
        if self.has_person_id(person.id):
            raise ValueError("Person already in People")
        self.people.append(person)
        debug("END")
    
    def has_conversation_id(self, conversation_id: str) -> bool:
        debug("START")
        for id in self.conversation_ids:
            if id == conversation_id:
                debug("END")
                return True
        debug("END")
        return False
    
    def add_conversation_id(self, conversation_id: str) -> None:
        debug("START")
        self.conversation_ids.add(conversation_id)
        debug("END")