from ai_models import GPT4O, GPT4, GPT3

# get flags for general pedo detections
# look through lists

#  Generated from GPT 4o
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

# "Requesting personal photos/videos",
# "Initiating conversations with minors",
# "Sending unsolicited explicit content",
# "Asking for personal information (address, phone number, etc.)",
# "Using suggestive or sexual language",
# "Trying to arrange in-person meetings",
# "Grooming behavior (flattery, promises, manipulation)",
# "Talking about age difference in a positive manner",
# "Requesting secrecy or hiding the chat",
# "Persistently messaging despite lack of response",
# "Creating a false identity (claiming to be younger)",
# "Engaging in role-playing with sexual undertones",
# "Sending gifts or money",
# "Threatening or blackmailing",
# "Using multiple accounts to contact the same person",
# "Frequent use of emojis or language to seem more relatable to minors",
# "Talking about or sharing links to inappropriate content",
# "Inquiring about the minor's relationship with parents or guardians",
# "Complimenting appearance excessively",
# "Discussing inappropriate topics for the minor's age"

# 0.8,0.6,0.7,0.9,0.9,0.8,0.6,1.0,0.7,0.8,1.0,0.9,0.7,1.0,0.8,0.9,0.9,0.7,0.6,0.8
