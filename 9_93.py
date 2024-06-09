import random
import string
from typing import Dict

wrd_li = string.ascii_lowercase


def gen_rand_name() -> str:
    name_len = random.randint(3, 6)
    return ''.join(random.choices(wrd_li, k=name_len))


def gen_rand_score() -> int:
    return random.randint(0, 99)


def gen_rand_dict() -> Dict[str, int]:
    s_d = {}

    for _ in range(5):
        s_d[gen_rand_name()] = gen_rand_score()

    return s_d


def gen_grade(grade: int) -> str:
    if not (0 <= grade <= 100):
        raise ValueError('Grade must be between 0 to 100')

    if grade > 90:
        return 'Outstanding'
    elif grade > 80:
        return 'Exceeds Expectations'
    elif grade > 70:
        return 'Meets Expectations'
    elif grade > 60:
        return 'Acceptable'
    else:
        return 'Fail'


if __name__ == '__main__':
    rand_dict = gen_rand_dict()
    print(rand_dict)

    graded_dict = {key: gen_grade(value) for key, value in rand_dict.items()}
    print(graded_dict)