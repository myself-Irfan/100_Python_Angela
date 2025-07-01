import os
import logging
from turtle import Turtle, Screen
from random import choice
import time


def setup_logging(file_name: str) -> None:
    """
    set up logging
    """

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(funcName)s | %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f'{file_name}.log')
        ]
    )

    logging.info('Logging setup complete')


class Paddle(Turtle):
    """
    paddle object
    """

    def __init__(self, screen_width: int, paddle_speed: int):
        logging.info(f'Initializing {self.__class__.__name__}')

        super().__init__()

        self.screen_width = screen_width
        self.paddle_speed = paddle_speed

        self.shape('square')
        self.color('white')
        self.shapesize(stretch_wid=1, stretch_len=5)
        self.penup()
        self.init_pos(-350)

        logging.info(f'{self.__class__.__name__} initialized successfully')

    def init_pos(self, y):
        logging.info('Initializing paddle position')
        self.goto(0, y)

    def go_left(self):
        if self.xcor() > - self.screen_width // 2 + 50:
            self.setx(self.xcor() - self.paddle_speed)

    def go_right(self):
        if self.xcor() < self.screen_width // 2 - 50:
            self.setx(self.xcor() + self.paddle_speed)


class Ball(Turtle):
    def __init__(self):
        logging.info(f'Initializing {self.__class__.__name__}')

        super().__init__()
        self.shape('circle')
        self.color('red')
        self.penup()

        self.dx = BALL_SPEED
        self.dy = BALL_SPEED

        self.init_pos(-250)

        logging.info(f'{self.__class__.__name__} initialized successfully')

    def init_pos(self, y):
        logging.info('Initializing ball position')
        self.goto(0, y)
        self.bounce_y()

    def move_ball(self):
        self.setx(self.xcor() + self.dx)
        self.sety(self.ycor() + self.dy)

    def bounce_x(self):
        self.dx *= -1

    def bounce_y(self):
        self.dy *= -1


class Brick(Turtle):
    def __init__(self, x, y, color: str):
        logging.info(f'Initializing {self.__class__.__name__}')

        super().__init__()
        self.shape('square')
        self.color(color)
        self.shapesize(stretch_wid=1, stretch_len=2)
        self.penup()
        self.goto(x, y)

        logging.info(f'{self.__class__.__name__} initialized successfully')


class Scoreboard(Turtle):
    def __init__(self):
        logging.info(f'Initializing {self.__class__.__name__}')

        super().__init__()
        self.score = 0
        self.color('white')
        self.penup()
        self.hideturtle()

        margin_x = -SCREEN_WIDTH // 2 + 20
        margin_y = SCREEN_HEIGHT // 2 - 40
        self.goto(margin_x, margin_y)
        self.update_score()

        logging.info(f'{self.__class__.__name__} initialized successfully')

    def update_score(self):
        self.clear()
        self.write(
            f'Score: {self.score}',
            align='left',
            font=('Arial', 20, 'normal')
        )

    def increase_score(self):
        logging.info('Increasing score')

        self.score += 1
        self.update_score()

    def game_over(self, message: str):
        self.goto(0, 0)
        self.write(
            message,
            align='center',
            font=("Arial", 20, "bold")
        )


class BreakOutGame:
    def __init__(self):
        logging.info(f'Initializing {self.__class__.__name__}')

        self.screen = Screen()
        self.screen.title('Game - Breakout')
        self.screen.bgcolor('black')
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.tracer(0)

        self.paddle = Paddle(SCREEN_WIDTH, PADDLE_SPEED)
        self.ball = Ball()
        self.scoreboard = Scoreboard()
        self.bricks = self._create_bricks()

        self._setup_controls()

        logging.info(f'{self.__class__.__name__} initialized successfully')

    def _create_bricks(self):
        logging.info(f'Initializing brick walls from {self.__class__.__name__}')

        bricks = []

        brick_width = BRICK_WIDTH
        brick_height = BRICK_HEIGHT
        brick_spacing_x = BRICK_SPACING_X
        brick_spacing_y = BRICK_SPACING_Y

        total_brick_width = brick_width + brick_spacing_x
        total_brick_height = brick_height + brick_spacing_y

        max_col = (SCREEN_WIDTH - 100) // total_brick_width
        max_row = (SCREEN_HEIGHT // 3) // total_brick_height

        start_x = -((max_col - 1) * total_brick_width) // 2
        start_y = SCREEN_HEIGHT // 2 - 80

        for row in range(max_row):
            for col in range(max_col):
                x = start_x + col * 60 # space b/w bricks
                y = start_y - row * 30
                color = choice(BRICK_COLORS)
                brick = Brick(x, y, color)
                bricks.append(brick)

        logging.info(f'Returning bricks from {self.__class__.__name__}')
        return bricks

    def _setup_controls(self):
        logging.info(f'Setting up controls')

        self.screen.listen()
        self.screen.onkeypress(self.paddle.go_left, "Left")
        self.screen.onkeypress(self.paddle.go_right, "Right")

        logging.info('Controls set up successfully')

    def run(self):
        game_on = True

        while game_on:
            self.screen.update()
            time.sleep(0.016) # 60 FPS
            self.ball.move_ball()

            # wall collisions
            if abs(self.ball.xcor()) > SCREEN_WIDTH // 2 - 10:
                self.ball.bounce_x()
            if self.ball.ycor() > SCREEN_HEIGHT // 2 - 10:
                self.ball.bounce_y()

            # paddle collisions
            if -350 < self.ball.ycor() < -340 and self.paddle.xcor() - 50 < self.ball.xcor() < self.paddle.xcor() + 50:
                self.ball.bounce_y()

            # bottom wall (lose condition)
            if self.ball.ycor() < -SCREEN_HEIGHT // 2:
                logging.info('Ball missed the paddle. Game over')
                self.scoreboard.game_over('GAME OVER')
                game_on = False

            # brick collision
            for brick in self.bricks[:]: # copy to avoid modifying list during iteration
                if self.ball.distance(brick) < 30:
                    self.ball.bounce_y()
                    brick.goto(1000, 1000)
                    self.bricks.remove(brick)
                    self.scoreboard.increase_score()
                    break

            # win condition
            if not self.bricks:
                logging.info('All bricks cleared. User won')
                self.scoreboard.game_over('YOU WIN')
                game_on = False

        self.screen.mainloop()


def main():
    setup_logging(CUR_FILE)

    game_instance = BreakOutGame()
    game_instance.run()


if __name__ == '__main__':
    CUR_FILE = os.path.splitext(os.path.basename(__file__))[0]

    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 800
    PADDLE_SPEED = 40
    BALL_SPEED = 3

    BRICK_COLORS = ["red", "orange", "yellow", "green", "blue"]

    BRICK_WIDTH = 40
    BRICK_HEIGHT = 20
    BRICK_SPACING_X = 20
    BRICK_SPACING_Y = 15

    main()