import random
from typing import List


def gen_rnd_crd() -> int:
    """return a random number between 2 and 11"""
    return random.randint(2, 11)


def gen_deck() -> List[int]:
    """return a shuffled deck of 52 cards"""

    new_deck = []
    while len(new_deck) < 52:
        rnd_crd = gen_rnd_crd()
        if rnd_crd == 10 and new_deck.count(10) < 16:
            new_deck.append(rnd_crd)
        elif new_deck.count(rnd_crd) < 4:
            new_deck.append(rnd_crd)
    random.shuffle(new_deck)
    return new_deck


def deal_card(cur_deck: List[int], hand: List[int]) -> None:
    """deals a card and removes said card from deck"""

    cur_card = random.choice(cur_deck)
    hand.append(cur_card)
    cur_deck.remove(cur_card)


def adj_hand(hand: List[int]) -> int:
    """takes a hand, calc sum and checks if has 11. if sum > 21 then changes the 11 to 1 and returns the final sum"""
    h_score = sum(hand)
    aces = hand.count(11)
    while h_score > 21 and aces:
        hand[hand.index(11)] = 1
        # h_score and aces are for while loop
        h_score -= 10
        aces -= 1
    return h_score


def get_stat() -> bool:
    """unless given Y/N it will repeatedly ask for an input"""
    while True:
        usr_in = input('Add card? Y/N: ').lower()
        if usr_in in ['y', 'n']:
            return usr_in == 'y'
        else:
            print('Input must be Y or N')


def compare(usr_score: int, bot_score: int) -> None:
    if usr_score > 21:
        print('User busts! Bot wins.')
    elif bot_score > 21 or usr_score > bot_score:
        print('User wins!')
    elif usr_score < bot_score:
        print('Bot wins')
    else:
        print('Draw!')


def game() -> None:
    usr_hand = []
    bot_hand = []

    cur_deck = gen_deck()
    print("Deck generated.")

    # init the game
    for _ in range(2):
        deal_card(cur_deck, usr_hand)
        deal_card(cur_deck, bot_hand)

    usr_score = adj_hand(usr_hand)
    bot_score = adj_hand(bot_hand)

    print(f'User hand: {usr_hand}, User score: {usr_score}')
    print(f'Bot hand: {bot_hand}, Bot score: {bot_score}')

    # if usr score is greater than 0 but less than 21
    while 0 < usr_score < 21:
        # if user returns yes
        if get_stat():
            deal_card(cur_deck, usr_hand)
            usr_score = adj_hand(usr_hand)
            print(f'User hand: {usr_hand}, User score: {usr_score}')
        else:
            break

    while bot_score < 17:
        deal_card(cur_deck, bot_hand)
        bot_score = adj_hand(bot_hand)
        print(f'Bot hand: {bot_hand}, Bot score: {bot_score}')

    compare(usr_score, bot_score)
    print(f'Final Score\nUser Score -> {usr_score}\nBot Score -> {bot_score}')


if __name__ == '__main__':
    try:
        while True:
            game()
            if input('Do you want to play again? Y/N: ').lower() != 'y':
                # if n then break else true so repeat game
                break
    except Exception as e:
        print(f'Error: {e}')