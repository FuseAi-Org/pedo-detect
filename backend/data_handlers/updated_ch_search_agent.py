# python3 -m backend.data_handlers.updated_ch_search_agent

from backend.ai_abstractions.ai_models import GPT4O
from backend.ai_abstractions.ai_prompts import prompt
from langchain.agents import tool
from .updated_ch_search_handler import search_episode, search_chat
from langchain.agents.format_scratchpad.openai_tools import (format_to_openai_tool_messages)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor

from backend.utils.debug_mode import debug

def get_search(identifier: str, search_type: str):
    @tool
    def search(query: str) -> int:
        """Tool to search within a specific episode or conversation"""
        if search_type == "episode":
            results = search_episode(int(identifier), query)
            return "\n".join(str(result[0].page_content) for result in results)
        elif search_type == "conversation":
            results = search_chat(identifier, query)
            return results
        else:
            raise ValueError("Invalid search_type. Use 'episode' or 'conversation'.")
    return search

SEARCH_AGENT = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | GPT4O.bind_tools([get_search("4", "episode")])
    | OpenAIToolsAgentOutputParser()
)

def get_search_agent_executor(identifier: str, search_type: str):    
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                #x["intermediate_steps"]
            ),
        }
        | prompt
        | GPT4O.bind_tools([get_search(identifier, search_type)])
        | OpenAIToolsAgentOutputParser()
    )
    return AgentExecutor(agent=agent, tools=[get_search(identifier, search_type)], verbose=True)

def get_search_agent_executor_for_chat(identifier: str, search_type: str):    
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),
        }
        | prompt
        | GPT4O.bind_tools([get_search(identifier, search_type)])
        | OpenAIToolsAgentOutputParser()
    )
    return AgentExecutor(agent=agent, tools=[get_search(identifier, search_type)], verbose=True)

# # Example usage for episode
# agent_executor = AgentExecutor(agent=SEARCH_AGENT, tools=[get_search("4", "episode")], verbose=True)
# output = list(agent_executor.stream({"input": "Is Speaker 3 a pedo?"}))
# for i in range(len(output)):
#     print(f"Output {i}:")
#     print(output[i])
#     print("\n")

# Example usage for conversation
agent_executor_chat = AgentExecutor(agent=SEARCH_AGENT, tools=[get_search("0a80df2434a267f6918e71b95d509b9b", "conversation")], verbose=True)
output_chat = list(agent_executor_chat.stream({"input": "Is a1e93f6891ceaab9619e0b276766b801 a pedo?"}))
debug(output_chat)
for i in range(len(output_chat)):
    print(f"Output {i}:")
    print(output_chat[i])
    print("\n")
