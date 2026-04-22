import sqlite3
import datetime
from tabulate import tabulate
from typing import Any

#checks if table exists
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
                        repetition INTEGER DEFAULT 0,
                        ease_factor REAL DEFAULT 2.5,
                        interval INTEGER DEFAULT 0,
                        next_review TEXT,
                        created_at TEXT,
                        updated_at TEXT,
                        FOREIGN KEY (deck_id) REFERENCES card_decks (id) ON DELETE CASCADE
                        )
                """)

def get_connection():
    connection = sqlite3.connect("card_deck.db")
    connection.row_factory = sqlite3.Row

    cursor =  connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    return connection

#adds a new deck to the card_decks table and returns its id
def create_deck(conn, name: str) -> int:
    cursor = conn.cursor()

    timestamp = datetime.datetime.now().isoformat()

    cursor.execute("INSERT INTO card_decks (name, created_at, updated_at) VALUES (?, ?, ?)", (name, timestamp, timestamp))

    if cursor.rowcount > 0:
        print(f"{name} was added.")

    conn.commit()
    return cursor.lastrowid

#removes a deck by id (also removes all cards in the deck)
def delete_deck(conn, deck_id: int) -> bool:
    cursor = conn.cursor()

    cursor.execute("DELETE FROM card_decks WHERE id = ?", (deck_id,))
    conn.commit()
    return cursor.rowcount > 0

#returns deck information
#returns all decks if no deck_id was passed
def get_deck(conn, deck_id: int = -1):
    cursor = conn.cursor()

    if deck_id == -1:
        cursor.execute("SELECT * FROM card_decks")
        return cursor.fetchall()

    cursor.execute("SELECT * FROM card_decks WHERE id = ?", (deck_id,))
    return cursor.fetchone()

#adds a new card to the cards table with the deck_id
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

    if cursor.rowcount > 0:
        print("\nCard added\n")

    conn.commit()

#removes a single card from the table by id
def delete_card(conn, card_id: int) -> bool:
    cursor = conn.cursor()

    cursor.execute("DELETE FROM cards WHERE id = ?", (card_id,))
    conn.commit()
    return cursor.rowcount > 0

#returns card information as a dictionary
def get_card(conn, card_id: int):
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cards WHERE id = ?", (card_id,))
    return cursor.fetchone()

#updates a decks name
def update_deck(conn, deck_id: int, new_name: str = ""):
    cursor = conn.cursor()

    timestamp = datetime.datetime.now().isoformat()
    
    if len(new_name) == 0:
        return "Error: Cannot update with no information."
    cursor.execute("UPDATE card_decks SET name = ?, update_at = ? WHERE id = ?", (new_name, timestamp, deck_id))

    conn.commit()
    return "Update Successful"

#returns the number of cards belonging to one deck
def get_num_cards_in_deck(conn, deck_id: int) -> int:
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM cards WHERE deck_id = ?", (deck_id,))
    count = cursor.fetchone()[0]
    return count

#updates a cards information
def update_card(conn, card_id: int, **kwargs) -> str:
    if not kwargs:
        return "Error: Cannot update with no information."

    allowed_keys = {"question", "answer", "deck_id"}
    updates = {key: value for key, value in kwargs.items() if key in allowed_keys and value}

    if not updates:
        return "Error: no valid fields to update."

    timestamp = datetime.datetime.now().isoformat()
    updates["updated_at"] = timestamp

    set_clause = ", ".join([f"{column} = ?" for column in updates.keys()])
    values = list(updates.values())
    values.append(card_id)

    sql = f"UPDATE cards SET {set_clause}  WHERE id = ?"

    cursor = conn.cursor()
    cursor.execute(sql, values)

    conn.commit()
    return "Update Successful"

#updates the time until the next review
def update_next_review(conn, card_id: int, new_sm2_data: tuple[int, float, int]) -> None:
    cursor = conn.cursor()
    
    new_repetition, new_ef, new_interval = new_sm2_data
    now = datetime.datetime.now()
    timestamp = now.isoformat()
    next_review_time = (now + datetime.timedelta(days=new_interval)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat()

    sql = "UPDATE cards SET repetition = ?, ease_factor = ?, interval = ?, next_review = ?, update_at = ? WHERE id = ?"
    data = (new_repetition, new_ef, new_interval, next_review_time, timestamp, card_id)
    cursor.execute(sql, data)

    conn.commit()

#returns cards that are due for review
def get_cards_for_review(conn):
    cursor = conn.cursor()

    now = datetime.datetime.now().isoformat()
    cursor.execute("SELECT * FROM cards WHERE next_review <= ?", (now,))

    return cursor.fetchall()

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

        print("\n*** Decks ***\n")
        print_table(connection, "card_decks")

        print("\n*** Cards ***\n")
        print_table(connection, "cards") 
    finally:
        connection.close()
