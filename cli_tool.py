from app.database import get_connection, initialize_db, create_deck, delete_deck, print_table, create_card, delete_card, get_card, get_deck

def main():

    connection = get_connection()

    try:

        initialize_db(connection)

        print("*** Card Table ***")
        print_table(connection, "card_decks")

        print("\n*** Cards ***")
        print_table(connection, "cards")

        print("\n*** Deck Info ***")
        print(get_deck(connection, 1))

        print("\n*** Card Info ***")
        print(get_card(connection, 1)["question"])

    finally:
        connection.close()

if __name__ == "__main__":
    main()
