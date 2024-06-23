import json
from typing import List
import os
from backend.utils.debug_mode import debug
from backend.utils.log_mode import set_log_mode
set_log_mode('test')

def get_global_data():
    with open('backend/flag_data/global_data.json', 'r') as file:
        data = json.load(file)
    num_pedos = data['num_pedos']
    flags = data['flags']
    weights = data['weights']
    return flags, num_pedos, weights

def set_global_data(flags: List[str], num_pedos:int, weights: List[List[float]]):
    data = {
        "num_pedos": num_pedos,
        'flags': flags,
        'weights': weights
    }
    with open('backend/flag_data/global_data.json', 'w') as file:
        json.dump(data, file)
    return 

print(get_global_data())

def get_single_account_data(account_id: str, include_flags=False):
    if not account_id.startswith('weights_'):
        account_id = f'weights_{account_id}'
    if not account_id.endswith('.json'):
        account_id = f'{account_id}.json'
    with open(f'backend/flag_data/account_flag_data/{account_id}', 'r') as file:
        data = json.load(file)
    weights = data['weights']
    is_pedo = data['is_pedo']
    return weights, is_pedo

def get_multi_account_data(account_id: List[str], pedos_only=False):
    output = []
    for account in account_id:
        weights, is_pedo = get_single_account_data(account, True)
        if pedos_only and is_pedo:
            output.append(weights)
        elif not pedos_only:
            output.append((weights, is_pedo))
    return output

def get_all_account_data(pedos_only=False, include_flags=False):
    data_path ='backend/flag_data/account_flag_data'
    files = [d for d in os.listdir(data_path) if not os.path.isdir(os.path.join(data_path, d))]
    return get_multi_account_data(files, pedos_only)


def avg(global_weights: List[List[float]]):
    debug("START")
    new_weights = []
    for i in range(len(global_weights)):
        new_weights.append(sum(global_weights[i])/len(global_weights))
    debug(new_weights, "END")
    return new_weights

def initialize_global_weights():
    print("INITIALIZING GLOBAL WEIGHTS")
    debug("START")
    flags, temp_num_pedos, weights = get_global_data()
    pedo_data = get_all_account_data(True,True)
    # global_weights = [[]]
    new_weights = []
    num_pedos = len(pedo_data)
    for i in range(num_pedos):
        pedo_weights = pedo_data[i]
        debug(pedo_weights)
        if i == 0:
            new_weights = [0 for _ in range(len(pedo_weights))]
        for j in range(len(pedo_weights)):
            debug(j, pedo_weights)
            curr_weights = pedo_weights[j]
            new_weights[j] += curr_weights / num_pedos
        debug(new_weights)
    debug(flags, num_pedos, new_weights)
    set_global_data(list(flags), num_pedos, new_weights)
    debug("END")
    return new_weights

def undo_avg(global_weights: List[List[float]], num_prior_pedos: int):
    debug("START")
    new_weights = []
    for i in range(len(global_weights)):
        new_weights.append(global_weights[i] * num_prior_pedos)
    debug(new_weights, "END")
    return new_weights

def weighted_avg(global_weights: List[float], num_pedos, new_weights: List[float]):
    debug("START", global_weights, num_pedos, new_weights)
    new_global_weights = []
    for i in range(len(global_weights)):
        debug(i, global_weights[i], new_weights[i])
        new_global_weights.append((global_weights[i] + new_weights[i])/(num_pedos+1))

    return new_global_weights
    

     

def update_global_weights_with_pedo(pedo_weights: List[float]):
    debug("START")
    global_flags, num_pedos, global_weights = get_global_data()
    new_weights = []
    # undone_weights = weight_inversion_function(global_weights, len(global_weights) - 1)
    for i in range(len(pedo_weights)):
    #     undone_weights[i] = [undone_weights[i], pedo_weights[i]]
        debug(global_weights[i], pedo_weights[i])
        new_weights.append(((global_weights[i] * num_pedos)+pedo_weights[i])/(num_pedos+1))
    
    # new_weights = weight_combination_function(undone_weights, num_pedos, pedo_weights)
    set_global_data(global_flags, num_pedos+1, new_weights)
    debug("END")
    return







# print(get_single_account_data('0a0d243b4c10d3a4fdb2669a4007fdce'))
# print(get_single_account_data('00aac10b39157377c79b7700b7b832bf'))
# print(get_single_account_data('0b6b05c740a1bf50ca7f9a461598a3b9'))
# print(get_multi_account_data(['0a0d243b4c10d3a4fdb2669a4007fdce', '00aac10b39157377c79b7700b7b832bf', '0b6b05c740a1bf50ca7f9a461598a3b9']))
# print(get_all_account_data())
# print(get_all_account_data(True)) 
# print(initialize_global_weights())
# print("GBD 1:", get_global_data()[1])
# print(update_global_weights_with_pedo([0.85, 0.82, 0.69, 0.8, 0.56, 0.07, 0.64, 0.29, 0.18, 0.01, 0.28, 0.57, 0.58, 0.86, 0.2, 0.77, 0.49, 0.22, 0.64, 0.29]))
# print("GBD 2:", get_global_data()[1])
initialize_global_weights()
print(get_global_data()[1])
update_global_weights_with_pedo([0.85, 0.82, 0.69, 0.8, 0.56, 0.07, 0.64, 0.29, 0.18, 0.01, 0.28, 0.57, 0.58, 0.86, 0.2, 0.77, 0.49, 0.22, 0.64, 0.29])
print(get_global_data())
update_global_weights_with_pedo([1, 0.82, 0.69, 0.8, 0.56, 0.07, 0.64, 0.29, 0.18, 0.01, 0.28, 0.57, 0.58, 0.86, 0.2, 0.77, 0.49, 0.22, 0.64, 0.29])
print(get_global_data())