# code-comment-to-trello-card
A tool that scans your software code for TODO comments, and creates Trello cards out of each.


## Software requirements:
No package installs are needed, other than python3

## To run:

From within the scan_targets.txt, type the relative paths for the code files you'd like monitored.
  You'll see todo_ex1 and todo_ex2 as sample python files, to show what it looks like.

Once that is done, fill in your parameters into the main.py script and run it
From there, it will run the code scrape and card creation based on your trello credentials and preferred comment flags.
