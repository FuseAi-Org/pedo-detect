from typing import Dict
import numpy as np

THRES = 0.3

def predict(flag_weights: Dict, account_weights: Dict):
    keys = list(flag_weights.keys())
    
    n = len(keys)

    # MAX_SCORE = np.dot(np.ones(n), np.ones(n))

    flag_weights = np.array([flag_weights[key] for key in keys])
    account_weights = np.array([account_weights[key] for key in keys])
    
    # score = np.dot(flag_weights, account_weights)

    # print("SCORE: ", score)
    # print("MAX :", MAX_SCORE)

    # return score / MAX_SCORE
    return weighted_average(flag_weights, account_weights)
    return dot_product(flag_weights, account_weights)

def dot_product(flag_vector, account_vector):
    MAX_SCORE = np.dot(np.ones(len(flag_vector)), np.ones(len(flag_vector)))

    print("DOT PRODUCT: ", np.dot(flag_vector, account_vector))
    print("MAX SCORE: ", MAX_SCORE)
    return np.dot(flag_vector, account_vector) / MAX_SCORE

def classify(flag_vector, account_vector):
    score = predict(flag_vector, account_vector)
    return score > THRES

def weighted_average(flag_vector, account_vector):
    total_weight = sum(flag_vector)
    normamlized_flag_vector = flag_vector / total_weight

    weighted_scores = normamlized_flag_vector * account_vector
    confidence = sum(weighted_scores)

    print("WEIGHTED AVERAGE: ", confidence)
    return confidence

# EXAMPLE USAGE
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

ACCOUNT_WEIGHTS = {
    "Requesting personal photos/videos": 0.85,
    "Initiating conversations with minors": 0.82,
    "Sending unsolicited explicit content": 0.69,
    "Asking for personal information (address, phone number, etc.)": 0.8,
    "Using suggestive or sexual language": 0.56,
    "Trying to arrange in-person meetings": 0.07,
    "Grooming behavior (flattery, promises, manipulation)": 0.64,
    "Talking about age difference in a positive manner": 0.29,
    "Requesting secrecy or hiding the chat": 0.18,
    "Persistently messaging despite lack of response": 0.01,
    "Creating a false identity (claiming to be younger)": 0.28,
    "Engaging in role-playing with sexual undertones": 0.57,
    "Sending gifts or money": 0.58,
    "Threatening or blackmailing": 0.86,
    "Using multiple accounts to contact the same person": 0.2,
    "Frequent use of emojis or language to seem more relatable to minors": 0.77,
    "Talking about or sharing links to inappropriate content": 0.49,
    "Inquiring about the minor's relationship with parents or guardians": 0.22,
    "Complimenting appearance excessively": 0.64,
    "Discussing inappropriate topics for the minor's age": 0.29
}

score = predict(FLAGS, ACCOUNT_WEIGHTS)
print(score)
