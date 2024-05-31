import random
import string
from typing import List

alpha_li = list(string.ascii_lowercase)


def gen_rand_wrd() -> List:
    rand_wrd = [random.choice(alpha_li) for _ in range(5)]

    return rand_wrd


def gen_usr_in() -> str:
    gen_usr_in = random.choice(alpha_li)

    return gen_usr_in.lower()


def ret_ans(usr_in: str, gen_wrd: List, dis_wrd: List) -> List:
    # index to access the cur index
    for index, _ in enumerate(gen_wrd):
        if usr_in == _:
            dis_wrd[index] = _
        else:
            pass

    return dis_wrd


if __name__ == '__main__':
    gen_wrd = gen_rand_wrd()
    #     print(gen_wrd)

    g = 0
    u_g = 0

    dis_wrd = ['_'] * len(gen_wrd)
    unique_g_wrd = set()

    while '_' in dis_wrd:
        usr_in = gen_usr_in()
        g += 1

        if usr_in in unique_g_wrd:
            # moves to next iteration
            continue

        unique_g_wrd.add(usr_in)
        u_g += 1

        dis_wrd = ret_ans(usr_in, gen_wrd, dis_wrd)
        #         print(''.join(dis_wrd))

    acc = round((u_g / g) * 100, 2)

    print(f'Total Tries: {g}')
    print(f'Unique Guess: {u_g}')
    print(f'Accuracy Rate: {acc}%')

