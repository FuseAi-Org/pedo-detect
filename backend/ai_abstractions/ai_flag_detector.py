from typing import Optional, List

from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI 
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.agents import AgentExecutor
from backend.ai_abstractions.ai_models import set_keys
import json

set_keys()

class Flag(BaseModel):
    """A flag with a description and a true or false value."""
    description: str
    value: bool

class FlagDetectorOutput(BaseModel):
    """List of flags output of the flag detector agent."""
    flags: list[Flag]

tools = []

llm = ChatOpenAI(
    model="gpt-4-1106-preview",
    temperature=0).with_structured_output(schema=FlagDetectorOutput)

prompt_template = PromptTemplate(
    input_variables=["chat_history", "flags"],
    template="""
System: You are an AI tasked with identifying inappropriate behavior in chat messages.

Below is a list of flags with their descriptions. Your job is to evaluate each chat message and determine if it violates any of these flags. Return a JSON object where the keys are the flag descriptions and the values are "True" or "False" indicating whether the message violates that flag.

Flags:
{flags}

Chat History:
{chat_history}

Evaluate the chat history and return the JSON object indicating whether each flag is violated.
"""
)


FLAGS = {
    "Requesting personal photos/videos": 0.9,
    "Initiating conversations with minors": 0.8,
    "Sending unsolicited explicit content": 1.0,
    "Asking for personal information (address, phone number, etc.)": 0.8,
    "Using suggestive or sexual language": 0.9,
    "Trying to arrange in-person meetings": 1.0,
    "Grooming behavior (flattery, promises, manipulation)": 0.9,
    "Talking about age difference in a positive manner": 0.7,
    "Requesting secrecy or hiding the chat": 0.8,
    "Persistently messaging despite lack of response": 0.6,
    "Creating a false identity (claiming to be younger)": 0.9,
    "Engaging in role-playing with sexual undertones": 0.8,
    "Sending gifts or money": 0.7,
    "Threatening or blackmailing": 1.0,
    "Using multiple accounts to contact the same person": 0.7,
    "Frequent use of emojis or language to seem more relatable to minors": 0.6,
    "Talking about or sharing links to inappropriate content": 0.9,
    "Inquiring about the minor's relationship with parents or guardians": 0.7,
    "Complimenting appearance excessively": 0.6,
    "Discussing inappropriate topics for the minor's age": 0.8
}

example_messages = [
        "da7885aa9fc3de1fd1bc0526796ced09 (08:59): hola",
        "b8a48b6e6c3a4db65e0dfabb41e95483 (08:59): hollla",
        "b8a48b6e6c3a4db65e0dfabb41e95483 (09:00): yo",
        "b8a48b6e6c3a4db65e0dfabb41e95483 (09:00): yoyo",
        "b8a48b6e6c3a4db65e0dfabb41e95483 (09:00): you type",
        "b8a48b6e6c3a4db65e0dfabb41e95483 (09:00): sloww",
        "b8a48b6e6c3a4db65e0dfabb41e95483 (09:00): akl;djlkjak",
        "da7885aa9fc3de1fd1bc0526796ced09 (09:00): this is kinda creepy haha your a &quot;stranger&quot;",
        "b8a48b6e6c3a4db65e0dfabb41e95483 (09:00): yes, yes I am",
        "da7885aa9fc3de1fd1bc0526796ced09 (09:00): i  was getting i stige",
        "da7885aa9fc3de1fd1bc0526796ced09 (09:00): stogge&apos;",
        "b8a48b6e6c3a4db65e0dfabb41e95483 (09:00): what&apos;s a stige? or.. stogge?",
        "da7885aa9fc3de1fd1bc0526796ced09 (09:01): cigarette",
        "b8a48b6e6c3a4db65e0dfabb41e95483 (09:01): ohh.",
        "b8a48b6e6c3a4db65e0dfabb41e95483 (09:01): where are you from?",
        "b8a48b6e6c3a4db65e0dfabb41e95483 (09:01): we just call them cigs here",
        "da7885aa9fc3de1fd1bc0526796ced09 (09:01): washington hbu",
        "b8a48b6e6c3a4db65e0dfabb41e95483 (09:01): lol",
        "b8a48b6e6c3a4db65e0dfabb41e95483 (09:01): canada",
        "da7885aa9fc3de1fd1bc0526796ced09 (09:01): sweet",
        "b8a48b6e6c3a4db65e0dfabb41e95483 (09:01): yep",
        "b8a48b6e6c3a4db65e0dfabb41e95483 (09:01): age?",
        "da7885aa9fc3de1fd1bc0526796ced09 (09:02): im 16  and a chick hbu",
        "da7885aa9fc3de1fd1bc0526796ced09 (09:02): my names stevi"
    ]

def output_parser(output: List[Flag]) -> list[Flag]:
    flags = {}
    for flag in output.flags:
        flags[flag.description] = flag.value
    return flags

agent = prompt_template | llm | output_parser

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)


# Example usage
response = agent.invoke({"chat_history": example_messages, "flags": FLAGS})
print(response, "\n")
print("-" * 50)




