import os
import logging
from random import randint


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(funcName)s | %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f'{FILE_NAME}.log')
        ]
    )


def init_list() -> list:
    return [DEFAULT_VAL for _ in range(9)]


def display_board(back_board: list) -> None:
    size = int(len(back_board) ** 0.5)

    print(f'Current State')
    for i in range(size):
        row = back_board[ i * size : (i + 1) * size]
        print("|".join(row))
        if i < size - 1:
            print("-" * (len(row) + 2))


def main():
    setup_logging()

    game_field = init_list()
    display_board(game_field)

    while DEFAULT_VAL in game_field:
        usr_in = int(input('User pos: ')) - 1
        game_field[usr_in] = 'O'
        game_field[randint(0, 9)] = 'X'
        display_board(game_field)


if __name__ == '__main__':
    FILE_NAME = os.path.splitext(os.path.basename(__file__))[0]
    DEFAULT_VAL = '_'

    main()