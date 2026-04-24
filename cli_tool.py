from app.database import get_connection, initialize_db, update_decks_for_review
from interface import choose_menu_action, review, review_card, edit_decks, study, study_cards, add, add_decks, add_cards, delete_decks, edit, edit_decks, edit_cards, delete, delete_cards
from states import Context, State

def main():

    connection = get_connection()
    ctx = Context(conn=connection)

    #maps the state to functions
    state_map: dict = {
            State.MAIN_MENU: choose_menu_action,
            State.SELECT_STUDY: study,
            State.REVIEW: review,
            State.REVIEW_CARD: review_card,
            State.STUDY: study_cards,
            State.SELECT_ADD: add,
            State.ADD_DECKS: add_decks,
            State.ADD_CARDS: add_cards,
            State.EDIT: edit,
            State.EDIT_DECKS: edit_decks,
            State.EDIT_CARDS: edit_cards,
            State.SELECT_DELETE: delete,
            State.DELETE_DECKS: delete_decks,
            State.DELETE_CARDS: delete_cards
            }

    try:

        initialize_db(connection)
        update_decks_for_review(connection)
        current_state = State.MAIN_MENU

        while current_state != State.EXIT:
            handler_function = state_map[current_state]
            current_state =  handler_function(ctx)

    finally:
        connection.close()

if __name__ == "__main__":
    main()
