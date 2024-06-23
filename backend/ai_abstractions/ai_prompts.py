from langchain.prompts import ChatPromptTemplate

flag_prompt = ChatPromptTemplate.from_template(\
    "You are an agent with the sole purpose of generating flags for identifying pedofiles via Instagram direct message history.\
    Flags are actions by the pedofile in chat that signal a high likelihood of being a pedofile.\
    Assign a flag weight for each flag, indicating how great of an indicator this flag is.\
    Return flags in the form of a dictionary with a string for the flag key and the flag weight for the value.\
        "
)
