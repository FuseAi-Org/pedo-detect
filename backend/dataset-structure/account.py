from typing import List, Dict

from conversation import Conversation
from ..ai_abstractions.flags import FLAGS

# ASSUPTION: Chat history is List[Tuple(username, text)]
class Account:
    def __init__(self, site_id: int, site_URL: str, attributes: Dict[str, str], username: str, conversations: List[Conversation]):
        self.site_id = site_id
        self.site_URL = site_URL
        self.attributes = attributes  # This should be a dictionary
        self.username = username
        self.conversations = conversations
        self.is_pedo = False
        self.flag_weights = {key: 0.0 for key in FLAGS} # Dict of weights for each flag/attribute, use smtg other than FLAGS when we migrate to attributes

    def update_global_flags(self, chat_history):
        # Update the account flags with the new set of flags 
        if self.is_pedo:
            pass
