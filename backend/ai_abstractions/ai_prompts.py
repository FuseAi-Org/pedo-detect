# from langchain.prompts import ChatPromptTemplate

# flag_prompt = ChatPromptTemplate.from_template(\
#     "You are an agent with the sole purpose of generating flags for identifying pedofiles via Instagram direct message history.\
#     Flags are actions by the pedofile in chat that signal a high likelihood of being a pedofile.\
#     Assign a flag weight for each flag, indicating how great of an indicator this flag is.\
#     Return flags in the form of a dictionary with a string for the flag key and the flag weight for the value.\
#         "
# )

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

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
