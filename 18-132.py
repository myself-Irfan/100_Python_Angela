from turtle import Turtle, Screen


def make_shape(turtle: Turtle, line_cnt: int) -> None:
    for _ in range(line_cnt):
        turtle.forward(50)
        turtle.left(int(360/line_cnt))


def draw_all(turtle: Turtle) -> None:
    for _ in range(3,11):
        print(f'Making shape with {_} lines')
        make_shape(turtle, _)


def draw_spirograph(turtle: Turtle, c_size: int, c_gap: int) -> None:
    """
    According to gap, will calculate how many iters/circle will be created
    :return: None
    """
    for _ in range(360//c_gap):
        turtle.circle(c_size)
        turtle.right(c_gap)
    print('Finished spirograph')


def main():
    i_screen = Screen()

    t1 = Turtle()
    t1.shape('turtle')
    t1.color('red')
    t1.speed('fastest')

    # draw_all(t1)
    draw_spirograph(t1, 50, 5)
    i_screen.exitonclick()


if __name__ == '__main__':
    main()
