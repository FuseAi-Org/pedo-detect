from typing import List, Tuple
from message import Message, MessageType
from datetime import datetime

class Conversation:
    def __init__(self, participants: Tuple, messages=List[Message], started_at=None, last_active=None):
        self.participants: Tuple = participants  # List of usernames involved in the chat
        self.messages: List[Message] = messages
        self.started_at = started_at  # Timestamp of when the conversation started
        self.last_active = last_active  # Timestamp of the last activity in the conversation

    def add_message(self, sender: str, recipient: str, text, timestamp: datetime, message_type: MessageType, media_url=None, read=False, replied_to=None):
        message = Message(sender, recipient, text, timestamp, message_type, media_url, read, replied_to)
        self.messages.append(message)
        self.last_active = timestamp

    def get_latest_messages(self, last_num_messages: int):
        if last_num_messages > len(self.messages) - 1:
            raise ValueError('last_num_messages must be less than or equal to the num of messages - 1')
        return self.messages[-last_num_messages] if self.messages else None

    def get_conversation_summary(self):
        # Future func is necessary
        pass

    def get_messages_by_user(self, username):
        return [msg for msg in self.messages if msg.sender == username]

    def __str__(self):
        return f"Conversation(participants={self.participants}, started_at={self.started_at}, last_active={self.last_active}, total_messages={len(self.messages)})"
