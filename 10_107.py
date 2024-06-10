import random
import string
from functools import wraps

sp_char = string.punctuation


def gen_rand_int() -> int:
    return random.randint(1, 10)


def gen_op() -> str:
    return random.choice(sp_char)


def check_zero(func):
    # preserve name & docstring
    @wraps(func)
    # replace og func
    def wrapper(x: int, y: int):
        if x == 0 or y == 0:
            raise ValueError('X/Y can not be 0')
        # calls the og func
        return func(x, y)

    return wrapper


def sort_int(func):
    # preserve name & docstring
    @wraps(func)
    # replace of func
    def wrapper(x: int, y: int):
        if x < y:
            x, y = y, x
        # calls the og func
        return func(x, y)

    return wrapper


def i_add(x: int, y: int) -> int:
    return x + y


@sort_int
def i_sub(x: int, y: int) -> int:
    return x - y


def i_mult(x: int, y: int) -> int:
    return x * y


@check_zero
@sort_int
def i_div(x: int, y: int) -> int:
    return int(x / y)


op = {
    '+': i_add,
    '-': i_sub,
    '*': i_mult,
    '/': i_div
}


def get_stat(stat: str) -> bool:
    if stat.upper() not in ['Y', 'N']:
        raise ValueError('Input must be Y/N')
    # if y then return True else False
    return stat.upper() == 'Y'


def main() -> None:
    x = gen_rand_int()

    shd_con = True

    while shd_con == True:
        y = ''
        while y not in ['+', '-', '*', '/']:
            y = gen_op()

        z = gen_rand_int()

        print(f'{x} {y} {z}')

        func = op[y]
        x = func(x, z)
        print(f'Ans -> {x}')

        shd_con = get_stat(input(f'Enter Y to continue with {x}: '))

    print(f'Final Ans: {x}')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Error: {e}')
