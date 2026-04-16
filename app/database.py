import sqlite3
import datetime
from tabulate import tabulate
from typing import Any

#check if table exists
def initialize_db(conn) -> None:
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS card_decks (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        created_at TEXT,
                        updated_at TEXT
                        )
                """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS cards (
                        id INTEGER PRIMARY KEY, 
                        deck_id INTEGER,
                        question TEXT NOT NULL,
                        answer TEXT NOT NULL,
                        ease_factor REAL DEFAULT 2.5,
                        interval INTEGER DEFAULT 0,
                        repetition INTEGER DEFAULT 0,
                        next_review TEXT,
                        created_at TEXT,
                        updated_at TEXT,
                        FOREIGN KEY (deck_id) REFERENCES card_decks (id) ON DELETE CASCADE
                        )
                """)

def get_connection():
    connection = sqlite3.connect("card_deck.db")
    cursor =  connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    return connection

#add a new deck to the card_decks table
def create_deck(conn, name: str) -> None:
    cursor = conn.cursor()

    now = datetime.datetime.now()
    timestamp = now.isoformat()

    cursor.execute("INSERT INTO card_decks (name, created_at, updated_at) VALUES (?, ?, ?)", (name, timestamp, timestamp))
    conn.commit()

#remove a deck by id
def delete_deck(conn, deck_id: int) -> bool:
    cursor = conn.cursor()

    cursor.execute("DELETE FROM card_decks WHERE id = ?", (deck_id,))
    conn.commit()
    return cursor.rowcount > 0

def create_card(conn, deck_id: int, question: str, answer: str) -> None:
    cursor = conn.cursor()

    now = datetime.datetime.now()
    timestamp = now.isoformat()

    cursor.execute("""INSERT INTO cards (
                       deck_id, question, answer, 
                       next_review, created_at, updated_at) 
                       VALUES (?, ?, ?, ?, ?, ?)""",
                   (deck_id, question, answer, timestamp, timestamp, timestamp)
                )
    conn.commit()

def delete_card(conn, card_id: int) -> bool:
    cursor = conn.cursor()

    cursor.execute("DELETE FROM cards WHERE id = ?", (card_id,))
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
    try: 
        initialize_db(connection)

        print_table(connection, "card_decks")
        print_table(connection, "cards") 
    finally:
        connection.close()
