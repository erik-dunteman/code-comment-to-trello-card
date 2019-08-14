import requests
import json



'''
Helper Utils_______________________________________________
'''


class TODO:
    def __init__(self, name, file_path, file_line):
        self.name = name
        self.file_path = file_path
        self.file_line = file_line
    def print(self):
        print(self.name, self.file_path, self.file_line)


def get_current_cards(key, secret, board_id):
    return_list = []
    url = "https://api.trello.com/1/boards/" + board_id
    querystring = {"actions":"all", "key": key, "token": secret}
    response = requests.request("GET", url, params=querystring)
    content = json.loads(response.content)
    actions = content['actions']
    for action in actions:
        try:
            data = action['data']
            # print(data)
            card_name = data['card']['name']
            return_list.append(card_name)
        except:
            pass
    return return_list

def scan_file(scan_targets_filepath, trigger):
    return_list = []
    
    # Sweep the scan_targets.txt file for filepaths
    filepaths = []
    with open(scan_targets_filepath, 'r') as file:
        for line in file:
            line = line.strip()
            filepaths.append(line)

    for filepath in filepaths:
        with open(filepath, 'r') as file:
            i = 1
            tl = len(trigger)
            for line in file:
                line = line.strip() # to remove leading and trailing whitespace, such as tabs and newlines
                truncate = line[:tl]
                if truncate == trigger:
                    name = line[tl+1:]
                    newTODO = TODO(name = name, file_path = filepath, file_line = i)
                    return_list.append(newTODO)
            i += 1
    return return_list


def add_card(todo, key, secret, board_id, list_id, timestamp):
    print("Adding: ", todo.name)
    description = "Comment found on line:\n{}\n\nof file:\n{}\n\nas of:\n{}".format(todo.file_line, todo.file_path, timestamp)
    url = "https://api.trello.com/1/lists/" + list_id + '/cards'
    querystring = {"key": key, "token": secret, 'name': todo.name, 'desc': description}
    response = requests.request("POST", url, params=querystring)
    





