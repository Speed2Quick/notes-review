from app.database import get_connection, initialize_db, create_deck, delete_deck, print_table, create_card, delete_card

def main():

    connection = get_connection()

    try:

        initialize_db(connection)

        print("*** Card Table ***")
        print_table(connection, "card_decks")

        print("\n*** Cards ***")
        print_table(connection, "cards")

    finally:
        connection.close()

if __name__ == "__main__":
    main()
