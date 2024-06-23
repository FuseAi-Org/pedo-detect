from backend.ai_abstractions.ai_models import GPT4O
from backend.ai_abstractions.ai_prompts import prompt
from langchain.agents import tool
from .ch_search_handler import search_episode
from langchain.agents.format_scratchpad.openai_tools import (format_to_openai_tool_messages)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor

def get_search(episode: int):
    @tool
    def search(query: str) -> int:
        """Tool to search within a specific episode"""
        results = search_episode(episode, query)
        return "\n".join(str(result[0].page_content) for result in results)
    return search

SEARCH_AGENT = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | GPT4O.bind_tools([get_search(4)])
    | OpenAIToolsAgentOutputParser()
)

def get_search_agent_executor(episode: int):    
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | GPT4O.bind_tools([get_search(episode)])
        | OpenAIToolsAgentOutputParser()
    )
    return AgentExecutor(agent=agent, tools=[get_search(episode)], verbose=True)

def get_search_agent_executor_for_chat(episode: int):    
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | GPT4O.bind_tools([get_search(episode)])
        | OpenAIToolsAgentOutputParser()
    )
    return AgentExecutor(agent=agent, tools=[get_search(episode)], verbose=True)

# agent_executor = AgentExecutor(agent=SEARCH_AGENT, tools=[get_search(4)], verbose=True)
# output = list(agent_executor.stream({"input": "Is Speaker 3 a pedo?"}))
# for i in range(len(output)):
#     print(f"Output {i}:")
#     print(output[i])
#     print("\n")