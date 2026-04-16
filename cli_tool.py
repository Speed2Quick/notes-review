from app.database import get_connection, initialize_db, create_deck, delete_deck, print_table

def main():

    connection = get_connection()

    try:

        initialize_db(connection)
        print_table(connection, "card_decks")

    finally:
        connection.close()

if __name__ == "__main__":
    main()
