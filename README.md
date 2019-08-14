# code-comment-to-trello-card
A tool that scans your software code for TODO comments, and creates Trello cards out of each.


## Software requirements:
No package installs are needed, other than python3

## To run:

From within the scan_targets.txt, type the relative paths for the code files you'd like monitored.
From within the scan_ignores.txt, you can ignore relative file paths, similar to .gitignore.

Once that is done, fill in your Trello parameters and preferred comment flags into the 
#### main.py 
script and run it.
From there, it will run the code scrape and card creation.


## Note:
The notation 'dir/*' in scan_targets or scan_ignores includes one level below 'dir', but no deeper. If any children of 'dir' are directories themselves, they'll be ignored.
