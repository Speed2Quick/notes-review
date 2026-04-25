from simple_term_menu import TerminalMenu
from sm2_logic import calculate_sm2
from database import create_deck, delete_deck, create_card, delete_card, get_card, get_deck, update_card, update_deck, update_cards_next_review_date, get_cards_for_review, update_decks_next_review, update_deck_next_review_date
from states import State
from datetime import datetime
import time
import os

#returns the state of the selected option
def choose_menu_action(ctx):
    clear_screen()

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
    clear_screen()
    update_decks_next_review(ctx.conn)
    ctx.deck_id = choose_deck(ctx)
    clear_screen()

    if ctx.deck_id == -1:
        return State.MAIN_MENU

    cards = get_cards_for_review(ctx.conn, ctx.deck_id)

    if len(cards) == 0:
        print("There are no cards to review in this deck", end="\r", flush=True)
        time.sleep(1)
        return State.MAIN_MENU

    days_until_review = float("inf")
    for index, card in enumerate(cards):
        print(f"Card #{index+1}/{len(cards)}")
        interval = review_card(ctx, card)

        if interval < days_until_review:
            days_until_review = interval

    next_review_date = update_deck_next_review_date(ctx.conn, days_until_review, ctx.deck_id)
    print(f"\nNext review on: {next_review_date}\n")

    choice = display_terminal_menu("Review another deck", "Menu")
    if choice == 0: return State.REVIEW
    return State.MAIN_MENU

#helper to review a card
def review_card(ctx, card):
    print(f"Question: {card["question"]}")
    

    display_terminal_menu("Flip")
    print(f"\nAnswer: {card["answer"]}")

    print("\n\nDifficulty: 0 hard | 5 easy")
    print("0 | 1 | 2 | 3 | 4 | 5\n")

    difficulty = int(input("Enter difficulty: "))
    while difficulty < 0 or difficulty > 5:
        print("\nPlease enter a number in the range of 0 to 5: ")
        difficulty = int(input("Enter difficulty: "))

    clear_screen()

    new_sm2 = calculate_sm2((card["repetition"], card["ease_factor"], card["interval"]), difficulty)
    update_cards_next_review_date(ctx.conn, card["id"], new_sm2)
    return new_sm2[2]

def study(ctx):
    ctx.deck_id = choose_deck(ctx)

    if ctx.card_id == -1:
        return State.MAIN_MENU

    return State.STUDY

def study_cards(ctx):
    ctx.card_id = choose_card(ctx)

    if ctx.card_id == -1:
        return State.SELECT_STUDY

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
    clear_screen()

    name: str = input("Enter a name for the deck: ")
    ctx.deck_id = create_deck(ctx.conn, name)

    if ctx.deck_id == -1:
        return State.MAIN_MENU
    
    choice = display_terminal_menu("Add another deck", "Add cards to new deck", "Menu")
    if choice == 0: return State.ADD_DECKS
    if choice == 1: return State.ADD_CARDS
    return State.MAIN_MENU

#helper to add cards
def add_cards(ctx):
    clear_screen()

    question, answer = set_card_info()
    create_card(ctx.conn, ctx.deck_id, question, answer)

    choice = display_terminal_menu("Add Another", "Menu")
    if choice == 0: return State.ADD_CARDS
    return State.MAIN_MENU

#updates deck name or card question and answer
def edit(ctx):
    print("Update deck or card?")
    choice = display_terminal_menu("Deck", "Card")
    clear_screen()

    if choice == 0: return State.EDIT_DECKS
    if choice == 1: 
        ctx.deck_id = choose_deck(ctx)
        clear_screen()

        if ctx.deck_id == -1:
            return State.MAIN_MENU

        return State.EDIT_CARDS
    return State.MAIN_MENU

#helper to update decks
def edit_decks(ctx):
    ctx.deck_id = choose_deck(ctx)
    clear_screen()

    if ctx.deck_id == -1:
        return State.MAIN_MENU

    name: str = input("Enter a new name for the deck: ")
    ctx.deck_id = update_deck(ctx.conn, ctx.deck_id, name)

    choice = display_terminal_menu("Update Another", "Menu")
    if choice == 0: return State.EDIT_DECKS
    return State.MAIN_MENU

#helper to update cards
def edit_cards(ctx):
    ctx.card_id = choose_card(ctx)
    clear_screen()

    if ctx.card_id == -1:
        return State.EDIT

    question, answer = set_card_info()
    update_card(ctx.conn, ctx.card_id, question=question, answer=answer)

    choice = display_terminal_menu("Back", "Update Another", "Menu")
    if choice == 0: return State.EDIT
    if choice == 1: return State.EDIT_CARDS
    return State.MAIN_MENU

#removes the selected deck or card from the database
def delete(ctx):

    print("Delete entire deck or a card:\n")
    choice = display_terminal_menu("Deck", "Card")
    clear_screen()

    if choice == 0: return State.DELETE_DECKS
    if choice == 1: 
        ctx.deck_id = choose_deck(ctx)

        if ctx.deck_id == -1:
            return State.MAIN_MENU

        return State.DELETE_CARDS
    return State.MAIN_MENU

#helper to delete deck
def delete_decks(ctx):
    ctx.deck_id = choose_deck(ctx)

    if ctx.deck_id == -1:
        return State.MAIN_MENU

    delete_deck(ctx.conn, ctx.deck_id)
    choice = display_terminal_menu("Delete another", "Menu")

    if choice == 0: return State.DELETE_DECKS
    return State.MAIN_MENU

#helper to delete card
def delete_cards(ctx):
    ctx.card_id = choose_card(ctx)

    if ctx.card_id == -1:
        return State.SELECT_DELETE

    delete_card(ctx.conn, ctx.card_id, ctx.deck_id)

    choice = display_terminal_menu("Delete another", "Menu")
    if choice == 0: return State.DELETE_CARDS
    return State.MAIN_MENU

#returns the deck id
def choose_deck(ctx):
    clear_screen()

    #gets id of selected deck
    decks = get_deck(ctx.conn)

    if len(decks) == 0:
        print("You have no decks", end="\r", flush=True)
        time.sleep(1)
        return -1

    deck_names: list[str] = []
    for index, deck in enumerate(decks):
        next_review_date = deck["next_review_date"]

        if deck["needs_review"] == True:
            deck_info = f"{index+1} **{deck["name"]}** ({deck["cards"]}) Next Review: {next_review_date}"
        else:
            deck_info = f"{index+1} {deck["name"]} ({deck["cards"]}) Next Review: {next_review_date}"
        deck_names.append(deck_info)
    print("Choose Deck:\n")
    choice = display_terminal_menu(*deck_names)

    if choice is None:
        return -1

    return decks[choice]["id"]

#returns the card id
def choose_card(ctx):
    clear_screen()

    #gets id of selected card
    cards = get_card(ctx.conn, deck_id=ctx.deck_id)

    if len(cards) == 0:
        print("You have no cards in this deck", end="\r", flush=True)
        time.sleep(1)
        return -1

    card_info: list[str] = [f"{index+1}. Question: {card["question"]}" for index, card in enumerate(cards)]
    print("Choose Card:\n")
    choice = display_terminal_menu(*card_info)

    if choice is None:
        return -1

    return cards[choice]["id"]

def get_question_answer(ctx):
    card = get_card(ctx.conn, card_id=ctx.card_id, deck_id=ctx.deck_id)
    return f"\nQuestion: {card["question"]}\nAnswer: {card["answer"]}\n"

#returns a user submitted question and answer
def set_card_info():
    question = input("Enter the question that will be displayed: ")
    answer = input("Enter the answer: ")
    clear_screen()
    return question, answer

#displays a menu and returns user input
def display_terminal_menu(*args):
    options: list[str] = [arg for arg in args]
    menu = TerminalMenu(options)
    return menu.show()

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    display_terminal_menu("1", "2", "3")
