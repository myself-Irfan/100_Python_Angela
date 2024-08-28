from turtle import Turtle, Screen
from time import sleep
from random import randint


class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('turtle')
        self.color('black')
        self.penup()
        self.setheading(90)
        self.reset_pos()
        self.mv_pace = MV_DIS

    def go_up(self):
        self.forward(self.mv_pace)

    def reset_pos(self):
        self.goto(START_POS)

    def is_at_finish(self):
        return self.ycor() > Y_FINISH


class CarI(Turtle):
    def __init__(self):
        super().__init__()
        self.shapesize(stretch_wid=1, stretch_len=2)
        self.shape('square')
        self.penup()
        self.color(self.rand_col())
        self.setheading(180)
        self.rand_gen()
        self.start_mv_dis = START_MV_DIS
        self.mv_incr = MV_INC

    def rand_col(self) -> tuple[int, int, int]:
        return randint(0, 255), randint(0, 255), randint(0, 255)

    def rand_gen(self):
        self.goto(SC_W // 2 - 20, randint(-250, 250))

    def mv_left(self):
        self.forward(self.start_mv_dis)

    def up_speed(self):
        self.start_mv_dis += self.mv_incr


class CarMgr:
    def __init__(self):
        self.car_li = []

    def add_car(self):
        # ensure once in every 6 iter
        if randint(1, 6) == 5:
            self.car_li.append(CarI())

    def mv_cars(self):
        for car in self.car_li:
            car.mv_left()

    def up_speed(self):
        for car in self.car_li:
            car.up_speed()


class ScoreBoard(Turtle):
    def __init__(self):
        super().__init__()
        self.color('black')
        self.penup()
        self.hideturtle()
        self.score = 0
        self.init_pos()
        self.w_score()

    def init_pos(self):
        self.goto(SC_W//2 - 50, SC_H//2 - 20)

    def w_score(self):
        self.clear()
        self.write(f'Score: {self.score}', align='center', font=FONT)

    def up_score(self):
        self.score += 1
        self.w_score()

    def game_over(self):
        self.goto(0, 0)
        self.write(f'GAME OVER', align='center', font=FONT)


class ScreenI:
    def __init__(self):
        self.screen = Screen()
        self.screen.setup(width=SC_W, height=SC_H)
        self.screen.tracer(0)
        self.screen.title('Turtle Cross')
        self.screen.colormode(255)
        self.sleep_time = SLP_T
        self.screen.listen()

    def refresh_scrn(self):
        sleep(self.sleep_time)
        self.screen.update()

    def terminate_scrn(self):
        self.screen.exitonclick()

    def bind_keys(self, turtle: Player):
        self.screen.onkey(turtle.go_up, 'Up')


def main():
    i_screen = ScreenI()
    i_turtle = Player()
    i_screen.bind_keys(i_turtle)
    i_carmgr = CarMgr()
    i_score = ScoreBoard()

    game_on = True

    while game_on:
        i_screen.refresh_scrn()

        # if player reaches upper border
        if i_turtle.is_at_finish():
            i_turtle.reset_pos()
            i_score.up_score()
            i_carmgr.up_speed()

        i_carmgr.add_car()
        i_carmgr.mv_cars()

        # turtle collision with car
        for car in i_carmgr.car_li:
            if car.distance(i_turtle) < 20:
                i_score.game_over()
                game_on = False

    i_screen.terminate_scrn()


if __name__ == '__main__':
    # player var
    START_POS = (0, -280)
    MV_DIS = 10
    Y_FINISH = 280

    # screen vars
    SC_W = 600
    SC_H = 600
    SLP_T = 0.1

    # car vars
    START_MV_DIS = 5
    MV_INC = 5

    # scoreboard var
    FONT = ('Courier', 10, 'normal')

    main()
