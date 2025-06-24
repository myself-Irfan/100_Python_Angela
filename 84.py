import os
import logging
from random import choice


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(funcName)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOG_FILENAME)
        ]
    )


class TicTacToe:
    def __init__(self, size: int):
        self.size = size
        self.board = [DEFAULT_VAL for _ in range(size * size)]
        logging.info(f"Initialized {size}x{size} board.")

    def display_board(self) -> None:
        print("\nCurrent State:\n")
        for i in range(self.size):
            row = self.board[i * self.size: (i + 1) * self.size]
            print(" | ".join(row))
            if i < self.size - 1:
                print("-" * (self.size * 4 - 3))

    def get_user_move(self) -> int:
        while True:
            try:
                move = int(input(f"Choose your move (1 to {len(self.board)}): ")) - 1
                if not 0 <= move < len(self.board):
                    print(f"{move + 1} is out of range.")
                elif self.board[move] != DEFAULT_VAL:
                    print(f"Cell {move + 1} is already taken.")
                else:
                    logging.info(f"User chose position {move + 1}")
                    return move
            except ValueError as e:
                logging.warning(f"Invalid user input: {e}")
                print("Please enter a valid number.")

    def get_computer_move(self) -> int:
        empty_cells = [i for i, cell in enumerate(self.board) if cell == DEFAULT_VAL]
        move = choice(empty_cells)
        logging.info(f"Computer chose position {move + 1}")
        return move

    def make_move(self, pos: int, symbol: str) -> None:
        self.board[pos] = symbol

    def check_win(self, symbol: str) -> bool:
        s = self.size

        # Check rows
        for i in range(s):
            if all(self.board[i * s + j] == symbol for j in range(s)):
                return True

        # Check columns
        for j in range(s):
            if all(self.board[j + i * s] == symbol for i in range(s)):
                return True

        # Check main diagonal
        if all(self.board[i * (s + 1)] == symbol for i in range(s)):
            return True

        # Check anti-diagonal
        if all(self.board[(i + 1) * (s - 1)] == symbol for i in range(s)):
            return True

        return False

    def is_draw(self) -> bool:
        return DEFAULT_VAL not in self.board


def main():
    setup_logging()

    try:
        size = int(input("Enter board size (e.g., 3 for 3x3): "))
        if size < 3:
            print("Minimum size is 3. Setting to 3.")
            size = 3
    except ValueError:
        print("Invalid input. Defaulting to 3x3.")
        size = 3

    game = TicTacToe(size)
    game.display_board()

    while True:
        # User move
        user_pos = game.get_user_move()
        game.make_move(user_pos, USER_SYMBOL)
        game.display_board()

        if game.check_win(USER_SYMBOL):
            print("🎉 You won!")
            break

        if game.is_draw():
            print("🤝 It's a draw!")
            break

        # Computer move
        comp_pos = game.get_computer_move()
        game.make_move(comp_pos, COMP_SYMBOL)
        game.display_board()

        if game.check_win(COMP_SYMBOL):
            print("💀 Enemy won!")
            break

        if game.is_draw():
            print("🤝 It's a draw!")
            break


if __name__ == '__main__':
    DEFAULT_VAL = '_'
    USER_SYMBOL = 'O'
    COMP_SYMBOL = 'X'
    LOG_FILENAME = os.path.splitext(os.path.basename(__file__))[0] + ".log"

    main()