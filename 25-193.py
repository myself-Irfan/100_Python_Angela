from turtle import Turtle, Screen
from pandas import read_csv, DataFrame
import logging
from time import sleep


class TurtleI(Turtle):
    def __init__(self):
        super().__init__()
        self.shape(IMG_F)


class ScreenI:
    def __init__(self):
        self.screen = Screen()
        self.screen.setup(750, 550)
        self.screen.title(SCR_T)
        self.screen.addshape(IMG_F)

    def scrn_in(self, score: int, attempt: int):
        return self.screen.textinput(title=f'{score}/{attempt}', prompt='Enter your guessed state\'s name').title()


class ScoreBoard(Turtle):
    def __init__(self):
        super().__init__()
        self.color('black')
        self.penup()
        self.hideturtle()
        self.attempt = 0
        self.score = 0

    def w_state(self, pos: tuple[int, int], state: str):
        self.goto(pos)
        self.write(state, align='center', font=FONT)
        logger.info(f'Successfully written {state} at {pos}')

    def in_attempt(self):
        self.attempt += 1

    def in_score(self):
        self.score += 1


def read_csv_f(in_f) -> DataFrame | None:
    try:
        logger.info('Reading csv...')
        in_cont = read_csv(in_f)

        if in_cont.empty:
            logger.warning(f'{in_f} is empty')
    except FileNotFoundError:
        in_cont = None
        logger.error(f'{in_f} not found in project dir')

    return in_cont


def return_pos(in_df: DataFrame, usr_in: str):
    row = in_df.loc[in_df['state'] == usr_in]
    return None if row.empty else int(row.iloc[0].x), int(row.iloc[0].y)


def main() -> None:
    in_df = read_csv_f(CSV_F)
    logger.info(f'Input DF has {in_df.shape}')

    i_screen = ScreenI()
    i_turtle = TurtleI()
    i_score = ScoreBoard()

    usr_in_li = []
    missing_li = []

    while len(usr_in_li) < 50:
        usr_in = i_screen.scrn_in(i_score.score, i_score.attempt)
        logger.info(f'Received input {usr_in}')
        if usr_in == 'Exit':
            logger.warning(f'User input is {usr_in}. Breaking loop')
            missing_li = [state for state in in_df.state if state not in usr_in_li]
            break
        elif usr_in in usr_in_li:
            logger.info(f'{usr_in} already added once')
        else:
            if in_df.state.isin([usr_in]).any():
                i_score.in_score()
                usr_in_li.append(usr_in)
                pos = return_pos(in_df, usr_in)
                logger.info(f'Calculated pos: {pos}')
                i_score.w_state(pos, usr_in)
                sleep(0.5)
            else:
                logger.warning(f'{usr_in} not found in dataframe')
        i_score.in_attempt()
    i_screen.screen.mainloop()

    print(missing_li)


if __name__ == '__main__':
    SCR_T = 'U.S. States'
    IMG_F = '25-193.gif'
    CSV_F = '25-193.csv'
    FONT = ('Courier', 10, 'normal')

    logging.basicConfig(
        format='%(asctime)s - %(levelname)s | %(message)s',
        level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    main()
