from turtle import Turtle, Screen
from random import randint


class TurtleI:
    def __init__(self, name: str, color: str):
        self.name = name
        self.turtle = Turtle()
        self.turtle.shape('turtle')
        self.turtle.color(color)
        self.turtle.penup()

    def init_pos(self, x: int, y: int) -> None:
        self.turtle.goto(x, y)

    def rand_fwd(self) -> None:
        self.turtle.forward(randint(1, 11))

    def check_finish(self, x_end: int) -> bool:
        return self.turtle.xcor() + 25 >= x_end

    def get_name(self) -> str:
        return self.name


def main():
    i_screen = Screen()
    i_screen.setup(width=500, height=400)

    i_w = i_screen.window_width() // 2
    i_h = i_screen.window_height() // 2

    usr_bet = i_screen.textinput(title="Choose your bet", prompt="Which turtle will win the race?(leonardo/raphael/donatello/michalangelo):")

    leonardo = TurtleI('leonardo', 'blue')
    raphael = TurtleI('raphael' ,'red')
    donatello = TurtleI('donatello', 'purple')
    michalangelo = TurtleI('michalangelo', 'orange')

    turtle_li = [leonardo, raphael, donatello, michalangelo]

    leonardo.init_pos((-i_w + 20), (-i_h + 50))
    raphael.init_pos((-i_w + 20), (-i_h + 150))
    donatello.init_pos((-i_w + 20), (-i_h + 250))
    michalangelo.init_pos((-i_w + 20), (-i_h + 350))

    w_name = ''
    race_on = True

    while race_on:
        for turtle in turtle_li:
            turtle.rand_fwd()
            if turtle.check_finish(i_w):
                w_name = turtle.get_name()
                race_on = False
                break

    i_screen.exitonclick()

    print(f'Winner is {w_name}')


if __name__ == '__main__':
    main()
