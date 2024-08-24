from turtle import Turtle, Screen


class TurtleCtrl:
    def __init__(self):
        self.i_turtle = Turtle()
        self.i_screen = Screen()
        self.i_screen.listen()

        self.i_screen.onkey(key="space", fun=self.mv_fwd)
        self.i_screen.onkey(key="Right", fun=self.pos_right)
        self.i_screen.onkey(key="Up", fun=self.pos_up)
        self.i_screen.onkey(key="Left", fun=self.pos_left)
        self.i_screen.onkey(key="Down", fun=self.pos_down)
        self.i_screen.onkey(key='c', fun=self.clear)

        self.i_screen.exitonclick()

    def pos_right(self):
        self.i_turtle.setheading(0)

    def pos_up(self):
        self.i_turtle.setheading(90)

    def pos_left(self):
        self.i_turtle.setheading(180)

    def pos_down(self):
        self.i_turtle.setheading(270)

    def mv_fwd(self) -> None:
        self.i_turtle.forward(10)

    def init_turtle(self) -> None:
        self.i_screen.exitonclick()

    def clear(self) -> None:
        self.i_turtle.penup()
        self.i_turtle.home()
        self.i_turtle.clear()
        self.i_turtle.pendown()


def main() -> None:
    print('Initiating Etch Turtle')
    TurtleCtrl()
    print('Terminating Etch Turtle')


if __name__ == '__main__':
    main()