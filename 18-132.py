from turtle import Turtle, Screen


def make_shape(turtle: Turtle, line_cnt: int) -> None:
    for _ in range(line_cnt):
        turtle.forward(200)
        turtle.right(int(360/line_cnt))


def main():
    i_screen = Screen()

    t1 = Turtle()
    t1.shape('turtle')
    t1.color('red')

    make_shape(t1, 5)

    i_screen.exitonclick()


if __name__ == '__main__':
    main()
