import sqlite3
from enum import Enum, auto
from dataclasses import dataclass

#tracks the state of the program
class State(Enum):
    MAIN_MENU = auto()
    SELECT_STUDY = auto()
    STUDY = auto()
    SELECT_ADD = auto()
    ADD_DECKS = auto()
    ADD_CARDS = auto()
    UPDATE = auto()
    SELECT_DELETE= auto()
    DELETE_DECKS = auto()
    DELETE_CARDS = auto()
    EXIT = auto()

#stores data to be passed into functions held by state
@dataclass
class Context:
    conn: sqlite3.Connection
    deck_id = None
    card_id = None

