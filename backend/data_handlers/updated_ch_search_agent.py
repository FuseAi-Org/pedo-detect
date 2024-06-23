# python3 -m backend.data_handlers.updated_ch_search_agent

from backend.ai_abstractions.ai_models import GPT4O
from backend.ai_abstractions.ai_prompts import prompt, bitch_prompt
from langchain.agents import tool
from .updated_ch_search_handler import search_episode, search_chat
from langchain.agents.format_scratchpad.openai_tools import (format_to_openai_tool_messages)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor

import json
import os

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
                x["intermediate_steps"]
            ),
        }
        | prompt
        | GPT4O.bind_tools([get_search(identifier, search_type)])
        | OpenAIToolsAgentOutputParser()
    )
    return AgentExecutor(agent=agent, tools=[get_search(identifier, search_type)], verbose=True)


# -----------------------------------------------

#     return messages
def get_message(output_chat):
    for key in output_chat:
        if key == "steps":
            for i in range(len(output_chat[key])):
                debug("GETMESSAGE: ", output_chat[key][i])
            return output_chat[key]

def get_search_agent_executor_for_chat(identifier: str):    
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                x["intermediate_steps"]
            ),  
        }
        | prompt
        | GPT4O.bind_tools([get_search(identifier, "conversation")]) 
        | OpenAIToolsAgentOutputParser()
    )
    return AgentExecutor(agent=agent, tools=[get_search(identifier, "conversation")], verbose=True) | get_message


# # Example usage for episode
# agent_executor = AgentExecutor(agent=SEARCH_AGENT, tools=[get_search("4", "episode")], verbose=True)
# output = list(agent_executor.stream({"input": "Is Speaker 3 a pedo?"}))
# for i in range(len(output)):
#     print(f"Output {i}:")
#     print(output[i])
#     print("\n")

# Example usage for conversation
# agent_executor_chat = AgentExecutor(agent=SEARCH_AGENT, tools=[get_search("0a80df2434a267f6918e71b95d509b9b", "conversation")], verbose=True)
# agent_executor_chat = get_search_agent_executor_for_chat("0a80df2434a267f6918e71b95d509b9b")
# output_chat = list(agent_executor_chat.stream({"input": "a1e93f6891ceaab9619e0b276766b801"}))

# debug(type(output_chat))
# debug(output_chat)

# debug(output_chat)
# for i in range(len(output_chat)):
#     print(f"Output {i}:")
#     print(output_chat[i])
#     print("\n")




def search_chat(conversation_id: str, query: str):
    data_path =f'././unzipped-data/parsed-pedo-chat-data/new-conversations/{conversation_id}.json'
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Conversation {conversation_id} does not exist")
    
    with open(data_path, 'r') as f:
        data = json.load(f)
        
        id = data['id']
        messages = json.dumps(data['messages'])
        person_ids = data['person_ids']

        agent = (
            bitch_prompt | GPT4O
        )

        return agent.invoke({"input": query, "chat_history": messages})
    
response = search_chat("0a80df2434a267f6918e71b95d509b9b", "a1e93f6891ceaab9619e0b276766b801")
print(response)
