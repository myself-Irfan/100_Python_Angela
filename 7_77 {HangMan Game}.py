import random
import string
from typing import List
import logging

alpha_li = list(string.ascii_lowercase)

W_L = 5


def gen_rand_wrd() -> List:
    rand_wrd = [random.choice(alpha_li) for _ in range(W_L)]

    return rand_wrd


def gen_usr_in() -> str:
    gen_usr_in = random.choice(alpha_li)

    return gen_usr_in.lower()


def ret_ans(usr_in: str, gen_wrd: List, blank_li: List[str]) -> List[str]:
    # index to access the cur index
    for index, _ in enumerate(gen_wrd):
        if usr_in == _:
            blank_li[index] = _
        else:
            pass

    return blank_li


def main():
    lives = 10
    score = 0
    t_g = 0

    gen_wrd = gen_rand_wrd()
    #     print(gen_wrd)

    blank_li = ['_'] * len(gen_wrd)
    #     print(blank_li)

    u_g = set()

    while lives > 0:
        usr_in = gen_usr_in()
        t_g += 1
        #         print(f'User chose -> {usr_in}')

        if usr_in in u_g:
            continue

        u_g.add(usr_in)

        blank_li = ret_ans(usr_in, gen_wrd, blank_li)
        #         print(f'Upon guess -> {blank_li}')

        if usr_in in gen_wrd:
            score += gen_wrd.count(usr_in)
        else:
            lives -= 1

        if '_' not in blank_li:
            logging.info('You win!!')
            break

    if '_' in blank_li:
        logging.info('LOST!')

    score = score + lives
    print('Scoreboard')
    print(f'Unique Vs Total -> {round((len(u_g) / t_g) * 100, 2)}%')
    print(f'Lives -> {lives}\nScore -> {score}\nFinal Answer -> {blank_li}')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s | %(message)s',
        handlers=[
            # logging.FileHandler('hangman-log.log'),
            logging.StreamHandler()
        ]
    )

    main()

