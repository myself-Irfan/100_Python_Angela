from turtle import Turtle, Screen
from time import sleep


class PaddleI(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('square')
        self.color('white')
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.penup()

    def init_pos(self, x):
        self.goto(x, 0)

    def go_up(self):
        if self.ycor() + 60 < SC_H//2:
            self.goto(self.xcor(), self.ycor() + 30)

    def go_down(self):
        if self.ycor() - 60 > - SC_H // 2:
            self.goto(self.xcor(), self.ycor() - 30)


class BallI(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('circle')
        self.color('blue')
        self.penup()
        self.x_move = 5
        self.y_move = 5
        self.sleep_sp = 0.05

    def move(self):
        self.bounce_y()
        self.goto(self.xcor()+self.x_move, self.ycor()+self.y_move)

    def bounce_y(self):
        """
        collision with top/bottom wall
        reverses y direction
        """
        if abs(self.ycor()) > SC_H // 2 - 20:
            self.y_move *= -1

    def bounce_x(self):
        self.x_move *= -1
        self.sleep_sp *= 0.9

    def reset_pos(self):
        self.sleep_sp = 0.05
        self.bounce_x()
        self.goto(0, 0)


class ScreenI:
    def __init__(self):
        self.screen = Screen()
        self.screen.setup(width=SC_W, height=SC_H)
        self.screen.bgcolor('black')
        self.screen.title('iPong')
        self.screen.tracer(0)
        self.screen.listen()

    def terminate_scrn(self):
        self.screen.exitonclick()

    def bind_keys(self, p1: PaddleI, p2: PaddleI):
        self.screen.onkey(p1.go_up, 'Up')
        self.screen.onkey(p1.go_down, 'Down')
        self.screen.onkey(p2.go_up, 'w')
        self.screen.onkey(p2.go_down, 's')


class ScoreBoard(Turtle):
    def __init__(self):
        super().__init__()
        self.color('white')
        self.penup()
        self.hideturtle()
        self.l_score = 0
        self.r_score = 0
        self.up_score()

    def up_score(self):
        self.clear()
        self.goto(-100, 225)
        self.write(self.l_score, align="center", font=('Courier', 50, 'normal'))
        self.goto(100, 225)
        self.write(self.r_score, align="center", font=('Courier', 50, 'normal'))

    def l_up_score(self):
        self.l_score += 1
        self.up_score()

    def r_up_score(self):
        self.r_score +=1
        self.up_score()


def main():
    i_screen = ScreenI()
    i_score = ScoreBoard()

    p1 = PaddleI()
    p1.init_pos(SC_W//2 - 20)
    p2 = PaddleI()
    p2.init_pos(-SC_W // 2 + 20)

    i_ball = BallI()

    i_screen.bind_keys(p1, p2)

    game_on = True
    while game_on:
        sleep(i_ball.sleep_sp)
        i_screen.screen.update()
        i_ball.move()

        if (i_ball.xcor() > 355 and i_ball.distance(p1) < 50) or (i_ball.xcor() < -355 and i_ball.distance(p2) < 50):
            i_ball.bounce_x()

        if i_ball.xcor() > 380:
            i_score.l_up_score()
            i_ball.reset_pos()

        if i_ball.xcor() < -380:
            i_score.r_up_score()
            i_ball.reset_pos()

    i_screen.terminate_scrn()


if __name__ == '__main__':
    SC_W = 800
    SC_H = 600

    main()