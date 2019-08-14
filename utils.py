import requests
import json
import glob
from os.path import isfile




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



# Get a list of cards on the board
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

# Add a card to the board
def add_card(todo, key, secret, board_id, list_id, timestamp):
    print("Adding: ", todo.name)
    description = "Comment found on line:\n{}\n\nof file:\n{}\n\nas of:\n{}".format(todo.file_line, todo.file_path, timestamp)
    url = "https://api.trello.com/1/lists/" + list_id + '/cards'
    querystring = {"key": key, "token": secret, 'name': todo.name, 'desc': description}
    response = requests.request("POST", url, params=querystring)
    



# Extract file/directory paths from the scan_targets and scan_ignores text files
def scan_file(targets_filepath, trigger):
    return_list = []
    
    # Sweep the scan_targets.txt file for filepaths
    filepaths = []
    with open(targets_filepath, 'r') as file:
        for line in file:
            line = line.strip()
            filepaths.append(line)
    return filepaths


# Take the paths from scan_file and expand them if "*" is included in the filepath. 
# Note: using "*"" in the filepath only goes one level deeper. Only direct children will be retrieved.
# Example: If within Dir1, I have [Dir2, file1, and file2], the expand_dirs('Dir1/*') will not include Dir2 or Dir2's contents.
def expand_dirs(filepaths):
    all_files = []
    for target in filepaths:
        subs = glob.glob(target)
        popdown = 0
        for i in range(len(subs)):
            i -= popdown
            if isfile(subs[i]) == False:
                subs.pop(i)
                popdown+=1
        all_files += subs
    return all_files


def get_todos(scan_targets, scan_ignores, trigger):
    
    # Get all target filepaths specified by scan_targets.txt
    all_targets = expand_dirs(scan_file(scan_targets, trigger))
    print("Considering: ", all_targets)
    print()

    # Get ignored filepaths specified by scan_ignores.txt
    all_ignores = expand_dirs(scan_file(scan_ignores, trigger))
    print("Ignoring: ", all_ignores)
    print()

    # Get filepaths only if they are targeted and not ignored
    targets = [item for item in all_targets if item not in all_ignores]
    
    # Dive into each target filepath to extract a TODO object
    return_list = []
    for filepath in targets:
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
    # Return list of TODO objects
    return return_list







