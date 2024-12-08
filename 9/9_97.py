import random
import string

wrd_li = string.ascii_lowercase


def gen_size() -> int:
    return random.randint(5, 10)


def gen_name() -> str:
    name_l = random.randint(3, 6)
    # generate k num str and join
    return ''.join(random.choices(wrd_li, k=name_l))


def gen_amt() -> int:
    return random.randint(10, 100)


def find_top(init_dict: dict) -> int:
    # Error handling if init dict is empty
    if not init_dict:
        raise ValueError('Initial Dictionary is empty')

    top_s = 0

    for _ in init_dict:
        if init_dict[_] > top_s:
            top_s = init_dict[_]

    return top_s


def find_win(init_dict: dict, top_s: int) -> dict[str, int]:
    win_dict = {}

    for _ in init_dict:
        if init_dict[_] == top_s:
            win_dict[_] = init_dict[_]

    return win_dict


if __name__ == '__main__':
    init_dict = {}

    s = gen_size()
    print(f'Size: {s}')

    for _ in range(s):
        name = gen_name()
        amt = gen_amt()

        init_dict[name] = amt

    print('Contenders')
    print(init_dict)

    top_s = find_top(init_dict)
    print(f'Top Score: {top_s}')

    print('Winner List')
    print(find_win(init_dict, top_s))
