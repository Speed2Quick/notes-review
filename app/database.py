import sqlite3
import datetime
from tabulate import tabulate
from typing import Any

#check if table exists
def initialize_db(conn) -> None:
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS card_decks (id INTEGER PRIMARY KEY, name TEXT, created_at TEXT, updated_at TEXT)")

def get_connection():
    return sqlite3.connect("card_deck.db")

#add a new deck to the card_decks table
def create_deck(conn, name: str) -> None:
    cursor = conn.cursor()

    now = datetime.datetime.now()
    timestamp = now.isoformat()

    cursor.execute("Insert INTO card_decks (name, created_at, updated_at) VALUES (?, ?, ?)", (name, timestamp, timestamp))
    conn.commit()

#remove a deck by id
def delete_deck(conn, id: int) -> bool:
    cursor = conn.cursor()

    cursor.execute("DELETE FROM card_decks WHERE id = ?", (id,))
    conn.commit()
    return cursor.rowcount > 0

def print_table(conn, name: str) -> None:
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {name}")

    rows: list[Any] = cursor.fetchall()
    headers: list[Any] = [description[0] for description in cursor.description]

    print(tabulate(rows, headers=headers, tablefmt="grid"))


if __name__ == "__main__":
    connection = get_connection()
    initialize_db(connection)

    print_table(connection, "card_decks")
