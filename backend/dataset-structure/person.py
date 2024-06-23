from typing import List, Dict
from account import Account

class Person:
    def __init__(self, person_id: int, relations: List[str], is_pedo: bool, pedo_score: int, attr: Dict[str, List], accounts: List[Account]) -> None:
        self.person_id = person_id
        self.relations = relations
        self.is_pedo = is_pedo
        self.pedo_score = pedo_score
        self.attributes = attr
        self.accounts = accounts