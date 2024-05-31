import random


def is_leap(year: int) -> bool:
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


if __name__ == '__main__':
    # year = int(input().strip())

    year = random.randint(1500, 2099)

    print(f'Is {year} a leap year? {is_leap(year)}')

