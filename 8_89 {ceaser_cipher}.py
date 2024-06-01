import string
import random
from typing import List

# alpha list
wrd_li = string.ascii_lowercase


def gen_shift_no() -> int:
    return random.randint(1, 26)


def gen_rand_wrd() -> List[str]:
    return [random.choice(wrd_li) for _ in range(5)]


def gen_encr_wrd(shift_wrd: int, gen_wrd: List[str]) -> List[str]:
    enc_wrd = []

    for _ in gen_wrd:
        init_ind = wrd_li.index(_)
        new_ind = (init_ind + shift_wrd) % len(wrd_li)
        enc_wrd.append(wrd_li[new_ind])

    return enc_wrd


def gen_dcrp_wrd(shift_wrd: int, enc_wrd: List[str]) -> List[str]:
    decr_wrd = []

    for _ in enc_wrd:
        init_ind = wrd_li.index(_)
        new_ind = (init_ind - shift_wrd) % len(wrd_li)
        decr_wrd.append(wrd_li[new_ind])

    return decr_wrd


if __name__ == '__main__':
    shift_no = gen_shift_no()
    print(f'User chose {shift_no}')
    gen_wrd = gen_rand_wrd()
    print(f'Your word {"".join(gen_wrd)}')

    encr_wrd = gen_encr_wrd(shift_no, gen_wrd)
    print(f'Encrypted Word -> {''.join(encr_wrd)}')

    decr_wrd = gen_dcrp_wrd(shift_no, encr_wrd)
    print(f'Decrypted Word -> {''.join(decr_wrd)}')

