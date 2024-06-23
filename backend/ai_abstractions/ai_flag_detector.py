from typing import Optional, List

from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI 
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.agents import AgentExecutor
from backend.ai_abstractions.ai_models import set_keys
import json
import os

set_keys()

class Flag(BaseModel):
    """A flag with a description and a confidence value between 0 and 1."""
    description: str
    value: float

class FlagDetectorOutput(BaseModel):
    """List of flags output of the flag detector agent."""
    flags: list[Flag]

tools = []

llm = ChatOpenAI(
    model="gpt-4-1106-preview",
    temperature=0).with_structured_output(schema=FlagDetectorOutput)


prompt_template = PromptTemplate(
    input_variables=["flags", "chat_history"],
    template="""
System:
You are an agent with the sole purpose of generating confidence scores for the flags that will be use for identifying pedofiles. \n
Flags are actions by the pedofile in chat that signal a high likelihood of being a pedofile. \n
Given a list of flags chat and chat history of all the messages, assign a flag weight for each flag, indicating how likely \n
of an indicator the magnitude of flag which is used to check the likelihood of how the chat message indicates being a pedophile.\ Return flags \n
in the form of a JSON object where the keys are the flag descriptions and the values are 0 to 1

Below is a list of flags with their descriptions and the chat history

Flags:
{flags}

Chat History:
{chat_history}

Evaluate the chat history and return the JSON object indicating whether each flag is violated.
"""
)


def output_parser(output: List[Flag]) -> list[Flag]:
    flags = {}
    for flag in output.flags:
        flags[flag.description] = flag.value
    return flags

agent = prompt_template | llm | output_parser

flags = ["Requesting personal photos/videos", "Initiating conversations with minors", "Sending unsolicited explicit content", "Asking for personal information (address, phone number, etc.)", "Using suggestive or sexual language", "Trying to arrange in-person meetings", "Grooming behavior (flattery, promises, manipulation)", "Talking about age difference in a positive manner", "Requesting secrecy or hiding the chat", "Persistently messaging despite lack of response", "Creating a false identity (claiming to be younger)", "Engaging in role-playing with sexual undertones", "Sending gifts or money", "Threatening or blackmailing", "Using multiple accounts to contact the same person", "Frequent use of emojis or language to seem more relatable to minors", "Talking about or sharing links to inappropriate content", "Inquiring about the minor's relationship with parents or guardians", "Complimenting appearance excessively", "Discussing inappropriate topics for the minor's age"]


def get_account_weights(conversation_id: str, flags: List[str]):
    data_path =f'././unzipped-data/parsed-pedo-chat-data/new-conversations/{conversation_id}.json'
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Conversation {conversation_id} does not exist")
    
    with open(data_path, 'r') as f:
        data = json.load(f)
        
        id = data['id']
        messages = json.dumps(data['messages'])
        person_ids = data['person_ids']

        agent = prompt_template | llm | output_parser

        return agent.invoke({"flags": flags, "chat_history": messages}) 


# response = get_account_weights("0a80df2434a267f6918e71b95d509b9b", flags)
# print(response)




