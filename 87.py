import os
import logging
from turtle import Turtle, Screen
import random
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

    def __init__(self, screen_width, paddle_speed):
        logging.info(f'Initializing {self.__class__.__name__}')

        super().__init__()

        self.screen_width = screen_width
        self.paddle_speed = paddle_speed

        self.shape('square')
        self.color('white')
        self.shapesize(stretch_wid=1, stretch_len=5)
        self.penup()
        self.init_pos(-250)

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

        self.init_pos(-200)

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
        self.goto(0, SCREEN_WIDTH//4)
        self.update_score()

        logging.info(f'{self.__class__.__name__} initialized successfully')

    def update_score(self):
        self.clear()
        self.write(
            f'Score: {self.score}',
            align='center',
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


def main():
    setup_logging(CUR_FILE)

    screen = Screen()
    screen.title('Game - Breakout')
    screen.bgcolor('black')
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.tracer(0)

    paddle = Paddle(SCREEN_WIDTH, PADDLE_SPEED)
    ball = Ball()
    scoreboard = Scoreboard()

    bricks = []
    start_x = -SCREEN_WIDTH // 2 + 50
    start_y = 200

    # initiating brick wall
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLUMNS):
            x = start_x + col * 60
            y = start_y + row * 30
            color = BRICK_COLORS[row % len(BRICK_COLORS)]
            brick = Brick(x, y, color)
            bricks.append(brick)

    screen.listen()
    screen.onkeypress(paddle.go_left, "Left")
    screen.onkeypress(paddle.go_right, "Right")

    game_on = True
    while game_on:
        screen.update()
        time.sleep(0.01)
        ball.move_ball()

        # wall collision
        if ball.xcor() > SCREEN_WIDTH // 2 - 10 or ball.xcor() < -SCREEN_WIDTH // 2 + 10:
            ball.bounce_x()
        if ball.ycor() > SCREEN_HEIGHT // 2 - 10:
            ball.bounce_y()

        # paddle collision
        if -240 < ball.ycor() < -230 and paddle.xcor() - 60 < ball.xcor() < paddle.xcor() + 60:
            ball.bounce_y()

        if ball.ycor() < -SCREEN_HEIGHT // 2:
            logging.info('Ball missed the paddle. Game over')
            scoreboard.game_over('GAME OVER')
            game_on = False

        for brick in bricks:
            if ball.distance(brick) < 35:
                ball.bounce_y()
                brick.goto(1000, 1000)
                bricks.remove(brick)
                scoreboard.increase_score()
                break

        # win condition
        if not bricks:
            logging.info('All bricks cleared. You win')
            scoreboard.game_over('YOU WIN!')
            game_on = False

    screen.mainloop()


if __name__ == '__main__':
    CUR_FILE = os.path.splitext(os.path.basename(__file__))[0]

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    PADDLE_SPEED = 40
    BALL_SPEED = 3

    BRICK_COLORS = ["red", "orange", "yellow", "green", "blue"]
    BRICK_ROWS = 4
    BRICK_COLUMNS = 12

    main()