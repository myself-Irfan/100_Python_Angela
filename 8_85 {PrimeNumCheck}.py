import random
from math import sqrt


def gen_end_no() -> int:
    # generate an abs num between 1 to 100
    return abs(random.randint(1, 100))


def check_prime(num: int) -> bool:

    if num < 2:
        # if 1 then not prime
        return False
    elif num < 4:
        # if 2 or 3 then prime
        return True
    elif num % 2 == 0:
        # optimization: if even then not prime
        return False
    else:
        # optimization: start with 3 till sqrt of num instead of num
        for n in range(3, int(sqrt(num)) + 1, 2):
            if num % n == 0:
                # if num clean divisible by any till sqrt(num) then not prime
                return False
        # if full loop executed then prime
        return True


if __name__ == '__main__':
    gen_no = gen_end_no()
    print(f'Checking {gen_no}')
    print(check_prime(gen_no))
