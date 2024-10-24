import random
from math import sqrt
import logging


def gen_end_no() -> int:
    # generate an abs num between 1 to 100
    return abs(random.randint(1, 100))


def check_prime(num: int) -> bool:

    if num < 2:
        # if 1 then not prime
        logging.info(f'Returning false for {num}')
        return False
    elif num < 4:
        # if 2 or 3 then prime
        logging.info(f'Returning true for {num}')
        return True
    elif num % 2 == 0:
        # optimization: if even then not prime
        logging.info(f'{num} % 2 == 0 as such returning false')
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
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            # logging.fileHandler('8-85.log'),
            logging.StreamHandler()
        ]
    )

    gen_no = gen_end_no()
    logging.info(f'{gen_no} is prime: {check_prime(gen_no)}')
