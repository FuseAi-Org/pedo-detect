from langchain_core.pydantic_v1 import BaseModel, Field
from .updated_ch_search_agent import get_search_agent_executor
from backend.ai_abstractions.ai_models import GPT4O
from backend.utils.debug_mode import debug
from typing import Optional

class YesNoResponse(BaseModel):
    """Final response to the question being asked"""
    answer: Optional[bool] = Field(default=False, description = "The final answer to respond to the user")


class YesNoAgent:
    def __init__(self, episode: int):
        self.agent_executor = get_search_agent_executor(episode)
    
    def get_response(self, query: str):
        # response = self.agent_executor(query)
        output = list(self.agent_executor.stream({"input": query}))
        return output[-1]["output"]
    
    def ask_yes_no(self, query: str) -> str:
        response = self.get_response(query)
        response = GPT4O.with_structured_output(YesNoResponse).invoke(
            f"You are a helpful assistant that converts query answers to a true/false. \
            The original query is: {query}\
            The final answer is: {response}\
            Assuming the final answer is correct, answer the query with true/false."
        )
        return response


# agent = YesNoAgent(20)
# # p = f"Is {person} {flag}?"
# print(agent.ask_yes_no("Does speaker 3 blackmail?"))


class ConfidenceResponse(BaseModel):
    """Final response to the question being asked"""
    answer: Optional[bool] = Field(default=False, description = "The final answer to respond to the user")
    confidence: Optional[float] = Field(default=0.5, description = "The confidence level of the final answer between 0 and 1 (0 = low confidence, 1 = high confidence)")

class ConfidenceAgent:
    def __init__(self, episode: int=1):
        self.agent_executor = get_search_agent_executor(episode)
    
    def get_response(self, query: str):
        # response = self.agent_executor(query)
        output = list(self.agent_executor.stream({"input": query}))
        return output[-1]["output"]
    
    def ask_confidence(self, query: str) -> str:
        response = self.get_response(query)
        response = GPT4O.with_structured_output(ConfidenceResponse).invoke(
            f"You are a helpful assistant that converts query answers to a confidence level. \
            The original query is: {query}\
            The final answer is: {response}\
            Assuming the final answer is correct, answer the query with a confidence level between 0 and 1."
        )
        return response

agent = ConfidenceAgent(20)
print(agent.ask_confidence("Does speaker 3 blackmail?"))
