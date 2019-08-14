key = "Your Trello Key"
secret = "Your Trello Secret Key"
board_id = "The ID of your target board"
list_id = "the ID of your target list, in which to drop new cards"
flag = "### TODO:" # or anything you'd like. If your files are not python, adjust this to follow suit with proper comment syntax in that language.
scan_targets = "scan_targets.txt"

from trelloTODO import run_comment_to_trello
run_comment_to_trello(key, secret, board_id, list_id, flag, scan_targets)