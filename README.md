# Personal Notes Review CLI App


## About

This is my first personal project on Boot.dev. I wanted to build a project that would allow me to learn control flow
and simple database management. I settled on an app that functions similarly to Anki but is used in the CLI. The project
took about a week to build. I have more ideas for improvements in the future, but I wanted to move on and learn more backend 
development and ML. 

### Tools
Python, SQLite

### Challenges
The largest challenge early on was designing the control flow. I settled on tracking different program states to minimize the
amount of conditional statements and confusion.

### What I Learned
I learned how important planning is when working on a project. Breaking down every task and developing a clear end goal made
everything much smoother. I also became more familiar with SQLite and making database queries.

## Features

### Review
This command allows you to select a deck of cards that is ready to be reviewed and review it. You're asked to give a score 0-5 for each
question you're asked. Those scores are fed into the sm2 algorithm to determine the next optimal review date.

### Study
This command allows you to look at the questions and answers on any deck.

### Add/Edit/Delete Cards/Deck
These commands allow you to add, edit, or delete entire decks or individual cards based on your input.


## Getting Started
- Prerequisites

  To get the project running on your machine, you'll need to have the following installed:

  Python 3.12.2 or higher

### Setup

    Clone the repository to your local machine:

git clone https://github.com/Speed2Quick/notes-review

    Change into the project directory:

cd notes-review

    Run cli_interface.py

python3 cli_interface.py
