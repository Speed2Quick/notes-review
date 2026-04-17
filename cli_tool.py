from app.database import get_connection, initialize_db, create_deck, delete_deck, print_table, create_card, delete_card, get_card, get_deck, update_next_review
from sm2_logic import calculate_sm2


def main():

    connection = get_connection()

    try:

        initialize_db(connection)

        card = get_card(connection, 1)
        current_sm2_data = (card["repetition"], card["ease_factor"], card["interval"])

        print("*** Current SM2 ***")
        print(current_sm2_data)

        new_sm2_data = calculate_sm2(current_sm2_data, 3)
        print("\n*** New Current SM2 ***")
        print(new_sm2_data)

        update_next_review(connection, 1, new_sm2_data)

        print("*** Card Table ***")
        print_table(connection, "card_decks")

        print("\n*** Cards ***")
        print_table(connection, "cards")

    finally:
        connection.close()

if __name__ == "__main__":
    main()
