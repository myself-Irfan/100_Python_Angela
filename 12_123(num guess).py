import random


def usr_diff() -> str:
    """A continuous loop which will only break when provided correct input"""
    while True:
        usr_in = input(
            'Please type \n"E" for easy\n"M" for medium\n"H" for hard\n"N" for cancel\nYour choice: ').upper()
        if usr_in in ['E', 'M', 'H', 'N']:
            return usr_in
        print("Invalid choice. Please enter 'E', 'M', 'H' or 'N'.")


def diff_tries(diff: str) -> int:
    """Return key value or 0 by default"""
    difficulties = {
        'E': 10,
        'M': 7,
        'H': 5
    }
    return difficulties.get(diff, 0)


def gen_rand_int() -> int:
    """Return a random number"""
    return random.randint(1, 10)


def get_usr_guess() -> int:
    """Runs a loop taking user input until proper input provided"""
    while True:
        usr_in = input('Please provide your guessed number (1-10) or type "N" to quit: ')
        if usr_in.lower() == 'n':
            print("Game cancelled. Goodbye!")
            # terminates the program entirely
            exit()
        try:
            usr_in = int(usr_in)
            if 1 <= usr_in <= 10:
                return usr_in
            else:
                raise ValueError
        except ValueError:
            print('Invalid input. Please enter a number between 1 to 10.')


def play_round(tries, rand_int):
    while tries > 0:
        usr_in = get_usr_guess()

        tries -= 1

        if usr_in == rand_int:
            print('Congratulations! You guessed the right number!')
            return True
        elif usr_in > rand_int:
            print('Too high.')
        else:
            print('Too low.')

        if tries > 0:
            print(f'You have {tries} {"tries" if tries > 1 else "try"} left.')
        else:
            print(f'Out of tries! The correct number was {rand_int}. Better luck next time!')

    return False


def play_game():
    print('Welcome to the Number Guessing Game!')

    usrDiff = usr_diff()

    if usrDiff == 'N':
        print("Game cancelled. Goodbye!")
        return

    tries = diff_tries(usrDiff)
    print(f'Difficulty: {usrDiff}\tTries: {tries}')

    rand_int = gen_rand_int()

    won = play_round(tries, rand_int)

    if won:
        print('You won')
    else:
        print('Better luck next time')


if __name__ == '__main__':
    play_game()
