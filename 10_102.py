import calendar
import random


def rand_int(medium: str) -> int:
    if medium.upper() not in ['Y', 'M']:
        raise ValueError('Only M or Y is accepted')
    elif medium.upper() == 'M':
        return random.randint(1, 12)
    else:
        return random.randint(1200, 2112)


def days_in_month(year: int, month: int) -> int:
    if not year or not month:
        raise ValueError('Year/Month can not be empty')

    _, num_d = calendar.monthrange(year, month)

    return num_d


def main() -> None:
    year = rand_int('y')
    print(year)
    month = rand_int('m')
    print(month)

    d = days_in_month(year, month)
    print(f'Num of days in {calendar.month_name[month]} in {year} is {d}')


if __name__ == '__main__':
    try:
        main()
    except ValueError as e:
        print(f'Error Occurred: {e}')