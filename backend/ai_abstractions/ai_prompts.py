# from langchain.prompts import ChatPromptTemplate

# flag_prompt = ChatPromptTemplate.from_template(\
#     "You are an agent with the sole purpose of generating flags for identifying pedofiles via Instagram direct message history.\
#     Flags are actions by the pedofile in chat that signal a high likelihood of being a pedofile.\
#     Assign a flag weight for each flag, indicating how great of an indicator this flag is.\
#     Return flags in the form of a dictionary with a string for the flag key and the flag weight for the value.\
#         "
# )

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate

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

# bitch_prompt = ChatPromptTemplate.from_messages(
#     [   
#         (
#             "system",
#             "You are an agent with the sole purpose of generating confidence scores for the flags that will be use for identifying pedofiles.\
#             Flags are actions by the pedofile in chat that signal a high likelihood of being a pedofile.\
#             Given a chat history of all the messages and an account id, assign a flag weight for each flag, indicating how likely of an indicator the magnitude of flag which is used to check the likelihood of how the chat message indicates being a pedophile.\ Return flags in the form of a dictionary with a string for the flag key and the flag weight for the value.\","
#         ),
#         ("account_id", "{id}"),
#         ("chat_history", "{chat_history}"),
#         MessagesPlaceholder(variable_name="agent_scratchpad"),
#     ]
# )

bitch_prompt = PromptTemplate(
    input_variables=["input", "chat_history"],
    template="""
    You are a helpful assistant. Use tools to answer the following prompt question. \n
    You are an agent with the sole purpose of generating confidence scores for the flags that will be use for identifying pedofiles. \n
    Flags are actions by the pedofile in chat that signal a high likelihood of being a pedofile. \n
    Given a a list of flags chat, an account id, and chat history of all the messagesassign a flag weight for each flag, indicating how likely \n
    of an indicator the magnitude of flag which is used to check the likelihood of how the chat message indicates being a pedophile.\ Return flags \n
    in the form of a dictionary with a string for the flag key and the flag weight for the value.,

    FLAGS: ["Requesting personal photos/videos", "Initiating conversations with minors", "Sending unsolicited explicit content", "Asking for personal information (address, phone number, etc.)", "Using suggestive or sexual language", "Trying to arrange in-person meetings", "Grooming behavior (flattery, promises, manipulation)", "Talking about age difference in a positive manner", "Requesting secrecy or hiding the chat", "Persistently messaging despite lack of response", "Creating a false identity (claiming to be younger)", "Engaging in role-playing with sexual undertones", "Sending gifts or money", "Threatening or blackmailing", "Using multiple accounts to contact the same person", "Frequent use of emojis or language to seem more relatable to minors", "Talking about or sharing links to inappropriate content", "Inquiring about the minor's relationship with parents or guardians", "Complimenting appearance excessively", "Discussing inappropriate topics for the minor's age"]
    
    ACCOUNT ID: {input} \n

    CHAT MESSAGE HISTORY: {chat_history}
    """
)
