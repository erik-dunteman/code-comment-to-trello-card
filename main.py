key = "Your Trello Key"
secret = "Your Trello Secret Key"
board_id = "The ID of your target board"
list_id = "the ID of your target list, in which to drop new cards"
trigger = "### TODO:" # or anything you'd like. If your files are not python, adjust this to follow suit with proper comment syntax in that language.
scan_targets = "scan_targets.txt"
scan_ignores = "scan_ignores.txt"


from datetime import date
from utils import TODO, get_current_cards, get_todos, add_card

'''
Main Function _________________________________________________
'''

def run_comment_to_trello(key, secret, board_id, list_id, trigger, scan_targets, scan_ignores):
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
        

        trigger 
            = the identifying string within your code, to indicate a TODO. For example, my lines start with "### TODO:"
        

        scan_targets 
            = the relative file path to the scan_targets.txt file, in which you specify the paths to all the code files you'd like scanned.

        scan_ignores
            = the relative file path to the scan_ignores.txt file, in which you specify the paths to all the code files you'd like to be ignored by the scan.

    '''

    # Get today's date, for timestamping
    timestamp = date.today()

    # Get the cards currently on your board (and archived)
    trello_todos = get_current_cards(key, secret, board_id)

    # Extract TODO objects from the files/directories designated by scan_targets.txt and scan_ignores.txt
    comment_todos = get_todos(scan_targets, scan_ignores, trigger)
    # Add a card for the TODOs, if they do not already exist
    for todo in comment_todos:
        if todo.name not in trello_todos:
            add_card(todo, key, secret, board_id, list_id, timestamp)
        else:
            print("Duplicate: ", todo.name)





'''
Main Script _________________________________________________
'''

run_comment_to_trello(key, secret, board_id, list_id, trigger, scan_targets, scan_ignores)