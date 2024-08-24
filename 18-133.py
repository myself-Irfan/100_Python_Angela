from turtle import Turtle, Screen
from random import choice, randint


def rand_dir():
    return choice([0, 90, 180, 270])


def rand_col() -> tuple[int, int, int]:
    return randint(0, 255), randint(0, 255), randint(0, 255)


def rand_p_size() -> int:
    return randint(1, 10)


def rand_move(turtle: Turtle) -> None:
    turtle.pencolor(rand_col())
    turtle.pensize(rand_p_size())
    turtle.setheading(rand_dir())
    turtle.forward(50)


def main():
    i_screen = Screen()
    i_screen.colormode(255)

    i_turtle = Turtle()
    i_turtle.speed('fastest')

    while True:
        rand_move(i_turtle)


if __name__ == '__main__':
    main()