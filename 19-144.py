from turtle import Turtle, Screen
from random import randint


class TurtleI:
    def __init__(self, color: str):
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


def main():
    i_screen = Screen()
    i_screen.setup(width=500, height=400)

    i_w = i_screen.window_width() // 2
    i_h = i_screen.window_height() // 2

    leonardo = TurtleI('blue')
    raphael = TurtleI('red')
    donatello = TurtleI('purple')
    michalangelo = TurtleI('orange')

    leonardo.init_pos((-i_w + 20), (-i_h + 50))
    raphael.init_pos((-i_w + 20), (-i_h + 150))
    donatello.init_pos((-i_w + 20), (-i_h + 250))
    michalangelo.init_pos((-i_w + 20), (-i_h + 350))

    while True:
        leonardo.rand_fwd()
        raphael.rand_fwd()
        donatello.rand_fwd()
        michalangelo.rand_fwd()

        if leonardo.check_finish(i_w) or raphael.check_finish(i_w) or donatello.check_finish(i_w) or michalangelo.check_finish(i_w):
            break

    i_screen.exitonclick()

if __name__ == '__main__':
    main()
