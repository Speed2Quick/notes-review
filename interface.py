from simple_term_menu import TerminalMenu
from app.database import create_deck, delete_deck, print_table, create_card, delete_card, get_card, get_deck, update_card, update_deck, update_next_review, get_cards_for_review, get_num_cards_in_deck
from states import State

#returns the state of the selected option
def choose_menu_action(ctx):
    choice = display_terminal_menu("Review", "Study", "Add a new card/deck", "Edit a card/deck", "Exit")

    #if choice == 0: return State.SELECT_DECK
    #if choice == 1: return State.SELECT_DECK
    if choice == 2: return State.SELECT_ADD
    if choice == 3: return State.UPDATE
    if choice == 4: return State.EXIT

def update_deck_or_card(ctx):
    choose_deck(ctx)

    print("Update deck or card?")
    choice = display_terminal_menu("Deck", "Card")

    if choice == 0:
        name: str = input("Enter a new name for the deck: ")
        ctx.deck_id = update_deck(ctx.conn, ctx.deck_id, name)
    if choice == 1:
        choose_card(ctx)
        question, answer = get_card_info()
        update_card(ctx.conn, ctx.card_id, question=question, answer=answer)

    choice = display_terminal_menu("Update Another", "Menu")
    if choice == 0: return State.UPDATE
    if choice == 1: return State.MAIN_MENU

#adds a new deck and cards or returns the state to select a deck to add to
def choose_deck_or_card(ctx):
    choice = display_terminal_menu("Deck", "Card")

    #adds a new deck and returns state to allow user to add cards to it
    if choice == 0:
        name: str = input("Enter a name for the deck: ")
        ctx.deck_id = create_deck(ctx.conn, name)
    else:
        choose_deck(ctx)
    return State.ADD_CARDS

#update the context deck id state
def choose_deck(ctx):
    #gets id of selected deck
    decks = get_deck(ctx.conn)
    deck_names: list[str] = [deck["name"] for deck in decks]
    choice = display_terminal_menu(*deck_names)

    ctx.deck_id = decks[choice]["id"]

#update the context card id state
def choose_card(ctx):
    #gets id of selected card
    cards = get_card(ctx.conn, deck_id=ctx.deck_id)
    card_info: list[str] = [card["question"] for card in cards]
    choice = display_terminal_menu(*card_info)

    ctx.card_id = cards[choice]["id"]

#adds cards until the user exits
def add_cards(ctx):
    question, answer = get_card_info()
    create_card(ctx.conn, ctx.deck_id, question, answer)

    choice = display_terminal_menu("Add Another", "Menu")
    if choice == 0: return State.ADD_CARDS
    if choice == 1: return State.MAIN_MENU

#returns a user submitted question and answer
def get_card_info():
    question = input("Enter the question that will be displayed: ")
    answer = input("Enter the answer: ")
    return question, answer

#displays a menu and returns user input
def display_terminal_menu(*args):
    options: list[str] = [arg for arg in args]
    menu = TerminalMenu(options)
    return menu.show()

if __name__ == "__main__":
    display_terminal_menu("1", "2", "3")
