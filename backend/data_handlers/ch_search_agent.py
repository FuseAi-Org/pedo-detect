from backend.ai_abstractions.ai_models import GPT4O
from langchain.agents import tool
from .ch_search_handler import search_episode
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
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

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Use tools (only if necessary) to best answer the users questions. You may use tools as many times as you need, but if you can't find the answer, you may give up.",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

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


# agent_executor = AgentExecutor(agent=SEARCH_AGENT, tools=[get_search(4)], verbose=True)
# output = list(agent_executor.stream({"input": "Is Speaker 3 a pedo?"}))
# for i in range(len(output)):
#     print(f"Output {i}:")
#     print(output[i])
#     print("\n")