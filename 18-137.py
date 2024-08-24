import turtle
from turtle import Turtle, Screen
from random import randint


def rand_col() -> tuple[int, int, int]:
    return randint(0, 255), randint(0, 255), randint(0, 255)


def init_pos(turtle: Turtle, scrn_w: int, scrn_h: int) -> None:
    init_x = - scrn_w + 20
    init_y = - scrn_h + 20
    turtle.setposition(init_x, init_y)


def gen_dot(turtle: Turtle):
    turtle.pendown()
    turtle.dot(20, rand_col())
    turtle.penup()


def main():
    i_screen = Screen()
    i_screen.colormode(255)

    i_w = i_screen.window_width() // 2
    i_h = i_screen.window_height() // 2

    i_turtle = Turtle()
    i_turtle.pensize(10)
    i_turtle.penup()

    init_pos(i_turtle, scrn_w=i_w, scrn_h=i_h)

    while i_turtle.ycor() < i_h:
        while -i_w < i_turtle.xcor() + 50 <= i_w:
            i_turtle.pendown()
            gen_dot(i_turtle)
            i_turtle.penup()
            i_turtle.forward(50)
        i_turtle.setposition(- i_w + 20, i_turtle.ycor() + 50)

    i_screen.exitonclick()


if __name__ == '__main__':
    main()