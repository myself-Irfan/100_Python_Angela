from turtle import Turtle, Screen


def make_shape(turtle: Turtle, line_cnt: int) -> None:
    for _ in range(line_cnt):
        turtle.forward(50)
        turtle.left(int(360/line_cnt))


def draw_all(turtle: Turtle) -> None:
    for _ in range(3,11):
        print(f'Making shape with {_} lines')
        make_shape(turtle, _)


def main():
    i_screen = Screen()

    t1 = Turtle()
    t1.shape('turtle')
    t1.color('red')

    draw_all(t1)

    i_screen.exitonclick()


if __name__ == '__main__':
    main()
