from simple_term_menu import TerminalMenu
from sm2_logic import calculate_sm2
from app.database import create_deck, delete_deck, print_table, create_card, delete_card, get_card, get_deck, update_card, update_deck, update_next_review, get_cards_for_review
from states import State

#add error handling if no card or deck is found
#refactor update to function similarly to add and delete


#returns the state of the selected option
def choose_menu_action(ctx):
    choice = display_terminal_menu("Review", "Study", "Add a new card/deck", "Edit a card/deck", "Delete a card/deck", "Exit")

    if choice == 0: return State.REVIEW
    if choice == 1: return State.SELECT_STUDY
    if choice == 2: return State.SELECT_ADD
    if choice == 3: return State.EDIT
    if choice == 4: return State.SELECT_DELETE
    if choice == 5: return State.EXIT
    return State.MAIN_MENU

#questions and receives answer from user, updating a cards next review time based on performance
def review(ctx):
    deck_id = choose_deck(ctx)
    cards = get_cards_for_review(ctx.conn, deck_id)

    for index, card in enumerate(cards):

        print(f"Card #{index+1}/{len(cards)}")

        review_card(ctx, card)

    choice = display_terminal_menu("Review another deck", "Menu")
    if choice == 0: return State.REVIEW
    return State.MAIN_MENU

#helper to review a card
def review_card(ctx, card):
    print(f"Question: {card["question"]}")
    

    display_terminal_menu("Flip")
    print(f"Answer: {card["answer"]}")

    print("Difficulty: 0 hard | 5 easy")
    print("0 | 1 | 2 | 3 | 4 | 5\n")
    difficulty = int(input("Enter difficulty: "))
    while difficulty < 0 or difficulty > 5:
        print("\nPlease enter a number in the range of 0 to 5: ")
        difficulty = int(input("Enter difficulty: "))

    new_sm2 = calculate_sm2((card["repetition"], card["ease_factor"], card["interval"]), difficulty)
    update_next_review(ctx.conn, card["id"], new_sm2)

def study(ctx):
    ctx.deck_id = choose_deck(ctx)
    return State.STUDY

def study_cards(ctx):
    ctx.card_id = choose_card(ctx)
    print(get_question_answer(ctx))

    choice = display_terminal_menu("Back", "Choose different deck", "Menu")

    if choice == 0: return State.STUDY
    if choice == 1: return State.SELECT_STUDY
    return State.MAIN_MENU

#adds a new deck and cards or returns the state to select a deck to add to
def add(ctx):
    choice = display_terminal_menu("Deck", "Card")

    #adds a new deck and returns state to allow user to add cards to it
    if choice == 0: return State.ADD_DECKS
    if choice == 1: 
        ctx.deck_id = choose_deck(ctx)
        return State.ADD_CARDS
    return State.MAIN_MENU

#helper to add deck
def add_decks(ctx):
    name: str = input("Enter a name for the deck: ")
    ctx.deck_id = create_deck(ctx.conn, name)
    
    choice = display_terminal_menu("Add another deck", "Add cards to new deck", "Menu")
    if choice == 0: return State.ADD_DECKS
    if choice == 1: return State.ADD_CARDS
    return State.MAIN_MENU

#helper to add cards
def add_cards(ctx):
    question, answer = set_card_info()
    create_card(ctx.conn, ctx.deck_id, question, answer)

    choice = display_terminal_menu("Add Another", "Menu")
    if choice == 0: return State.ADD_CARDS
    return State.MAIN_MENU

#updates deck name or card question and answer
def edit(ctx):
    print("Update deck or card?")
    choice = display_terminal_menu("Deck", "Card")

    if choice == 0: return State.EDIT_DECKS
    if choice == 1: 
        ctx.deck_id = choose_deck(ctx)
        return State.EDIT_CARDS
    return State.MAIN_MENU

#helper to update decks
def edit_decks(ctx):
    ctx.deck_id = choose_deck(ctx)
    name: str = input("Enter a new name for the deck: ")
    ctx.deck_id = update_deck(ctx.conn, ctx.deck_id, name)

    choice = display_terminal_menu("Update Another", "Menu")
    if choice == 0: return State.EDIT_DECKS
    return State.MAIN_MENU

#helper to update cards
def edit_cards(ctx):
    ctx.card_id = choose_card(ctx)
    question, answer = set_card_info()
    update_card(ctx.conn, ctx.card_id, question=question, answer=answer)

    choice = display_terminal_menu("Back", "Update Another", "Menu")
    if choice == 0: return State.EDIT
    if choice == 1: return State.EDIT_CARDS
    return State.MAIN_MENU

#removes the selected deck or card from the database
def delete(ctx):

    print("Delete entire deck or a card")
    choice = display_terminal_menu("Deck", "Card")

    if choice == 0: return State.DELETE_DECKS
    if choice == 1: 
        ctx.deck_id = choose_deck(ctx)
        return State.DELETE_CARDS
    return State.MAIN_MENU

#helper to delete deck
def delete_decks(ctx):
    ctx.deck_id = choose_deck(ctx)
    delete_deck(ctx.conn, ctx.deck_id)
    choice = display_terminal_menu("Delete another", "Menu")

    if choice == 0: return State.DELETE_DECKS
    return State.MAIN_MENU

#helper to delete card
def delete_cards(ctx):
    ctx.card_id = choose_card(ctx)
    delete_card(ctx.conn, ctx.card_id)

    choice = display_terminal_menu("Delete another", "Menu")

    if choice == 0: return State.DELETE_CARDS
    return State.MAIN_MENU

#returns the deck id
def choose_deck(ctx):
    #gets id of selected deck
    decks = get_deck(ctx.conn)
    deck_names: list[str] = [f"{index+1}. {deck["name"]} ({deck["cards"]})" for index, deck in enumerate(decks)]
    choice = display_terminal_menu(*deck_names)

    return decks[choice]["id"]

#returns the card id
def choose_card(ctx):
    #gets id of selected card
    cards = get_card(ctx.conn, deck_id=ctx.deck_id)
    card_info: list[str] = [f"{index+1}. Question: {card["question"]}" for index, card in enumerate(cards)]
    choice = display_terminal_menu(*card_info)

    return cards[choice]["id"]

def get_question_answer(ctx):
    card = get_card(ctx.conn, card_id=ctx.card_id, deck_id=ctx.deck_id)
    return f"\nQuestion: {card["question"]}\nAnswer: {card["answer"]}\n"

#returns a user submitted question and answer
def set_card_info():
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
