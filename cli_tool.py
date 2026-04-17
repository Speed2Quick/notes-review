from sqlite3 import connect
from app.database import get_connection, initialize_db, create_deck, delete_deck, print_table, create_card, delete_card, get_card, get_deck, update_next_review, get_cards_for_review, get_num_cards_in_deck
from sm2_logic import calculate_sm2
import datetime


def main():

    connection = get_connection()

    try:

        initialize_db(connection)


    finally:
        connection.close()

if __name__ == "__main__":
    main()
