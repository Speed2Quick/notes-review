#repetition = current winning streak
#interval = how many days until the card should be given
#ease_factor = multiplier to determine when the card should be shown again
#score = how difficult the question was (1-2 means an incorrect answer was given)

#calculates and returns the new values for repetition, ef, and interval
def calculate_sm2(current_sm2_data: tuple[int, float, int], score: int) -> tuple[int, float, int]:
    
    current_repetition, current_ef, current_interval, = current_sm2_data

    #calculate ease factor making sure it's a minimum of 1.3
    new_ef: float = current_ef + (0.1 - (5 - score) * (0.08 + (5 - score) * 0.02))
    new_ef = max(1.3, new_ef)

    #wrong answer
    if score < 3:
        new_interval: int = 1
        new_repetition: int = 0
    else:
        new_repetition: int = current_repetition + 1
        #first time getting correct
        if new_repetition == 1:
            new_interval: int = 1
        #correct for second time in a row
        elif new_repetition == 2:
            new_interval: int = 6
        #correct multiple times in a row
        else:
            new_interval: int = round(current_interval * new_ef)  
    return new_repetition, new_ef, new_interval
