from app.database import get_connection, initialize_db
from interface import choose_menu_action, choose_deck_or_card, choose_deck, get_card_info, add_cards
from states import Context, State

def main():

    connection = get_connection()
    ctx = Context(conn=connection)

    #maps the state to functions
    state_map: dict = {
            State.MAIN_MENU: choose_menu_action,
            State.SELECT_ADD: choose_deck_or_card,
            State.ADD_CARDS: add_cards
            }

    try:

        initialize_db(connection)
        current_state = State.MAIN_MENU

        while current_state != State.EXIT:
            handler_function = state_map[current_state]
            current_state =  handler_function(ctx)

    finally:
        connection.close()

if __name__ == "__main__":
    main()
