import requests
import json
from datetime import date

'''
Main Function_________________________________________________
'''

def run_comment_to_trello(key, secret, board_id, list_id, flag, scan_targets):
    '''
    input parameters:
        
        key 
            = your trello user account key, found at https://trello.com/app-key
        

        secret 
            = your trello user secret key, found through the above link by clicking the "generate a Token" link
        

        board_id 
            = the id of your board, found at www.trello.com/b/{board_id}/board_name
        

        list_id 
            = the id of the list, found by looking at the json format of the board of interest (add ".json" to the end of the board url to see).
        

        flag 
            = the identifying string within your code, to indicate a TODO. For example, my lines start with "### TODO:"
        

        scan_targets 
            = the relative file path to the scan_targets.txt file, in which you specify the paths to all the code files you'd like scanned.

    '''

    # Get today's date, for timestamping
    timestamp = date.today()

    # Get the cards currently on your board (and archived)
    trello_todos = get_current_cards(key, secret, board_id)

    # Extract TODO objects from the scan_targets.txt file and the respective code files
    comment_todos = scan_file(scan_targets, flag)

    # Add a card for the TODOs, if they do not already exist
    for todo in comment_todos:
        if todo.name not in trello_todos:
            add_card(todo, key, secret, board_id, list_id, timestamp)
        else:
            print("Duplicate: ", todo.name)








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
    





