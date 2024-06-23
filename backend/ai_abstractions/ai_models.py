import os
from langchain_openai import ChatOpenAI

def set_keys():
    os.environ["OPENAI_API_KEY"] = 'sk-proj-wFCaJMaXtsVKWaMiYxhKT3BlbkFJImWFT5KiMpPCOnSvtPe9'
    os.environ["TAVILY_API_KEY"] = "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"

set_keys()

GPT3 = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
)

GPT4 = ChatOpenAI(
    model="gpt-4-1106-preview",
    temperature=0,
)

GPT4O = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
)
