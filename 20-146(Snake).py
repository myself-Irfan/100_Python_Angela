from turtle import Turtle, Screen
from time import sleep
from random import randint


class TurtleI(Turtle):
    def __init__(self, color: str, shape: str) -> None:
        """
        initializing a Turtle obj/Snake dot with attributes
        :return: None
        """
        super().__init__()
        self.color(color)
        self.shape(shape)
        self.penup()


class SnakeI:
    def __init__(self) -> None:
        """
        init a Snake obj
        has segments which is initialized by calling method
        head is the first item in segments
        :return: None
        """
        self.segments = []
        self.create_snake()
        self.head = self.segments[0]

    def create_snake(self) -> None:
        """
        adds a turtle obj to snake attrb segments
        :return: None
        """
        for pos in START_POS:
            self.add_segment(pos)

    def add_segment(self, pos):
        seg = TurtleI('white', 'square')
        seg.goto(pos)
        self.segments.append(seg)

    def extend(self):
        self.add_segment(self.segments[-1].position())

    def move(self) -> None:
        """
        move segment in reverse order replacing each dot pos with prev pos
        and upon loop completion moves the head forward
        :return: None
        """
        for seg in range(len(self.segments) - 1, 0, -1):
            nw_x = self.segments[seg - 1].xcor()
            nw_y = self.segments[seg - 1].ycor()
            self.segments[seg].goto(nw_x, nw_y)
        self.head.forward(PACE)

    def right(self) -> None:
        """
        if turtle is not going left
        set heading to right
        :return: None
        """
        if self.head.heading() != 180:
            self.head.setheading(0)

    def up(self) -> None:
        if self.head.heading() != 270:
            self.head.setheading(90)

    def left(self) -> None:
        if self.head.heading() != 0:
            self.head.setheading(180)

    def down(self) -> None:
        if self.head.heading() != 90:
            self.head.setheading(270)


class FoodI(TurtleI):
    def __init__(self):
        super().__init__('blue', 'circle')
        self.shapesize(stretch_len=0.5, stretch_wid=0.5)
        self.speed('fastest')
        self.goto_rand_pos()

    def gen_rand_pos(self) -> tuple[int, int]:
        return randint(-250, 250), randint(-250, 250)

    def goto_rand_pos(self):
        self.goto(self.gen_rand_pos())


class ScreenI:
    def __init__(self):
        """
        Inits Screen obj
        """
        self.screen = Screen()
        self.screen.setup(width=SC_W, height=SC_H)
        self.screen.bgcolor('black')
        self.screen.title('iSnake')
        self.screen.tracer(0)
        self.screen.listen()
        self.draw_border()

    def bind_keys(self, snake: SnakeI) -> None:
        """
        Maps key action with defined custom turtle functions
        :return: None
        """
        self.screen.onkey(snake.up, "Up")
        self.screen.onkey(snake.down, "Down")
        self.screen.onkey(snake.left, "Left")
        self.screen.onkey(snake.right, "Right")

    def draw_border(self):
        border_turtle = TurtleI('white', 'arrow')
        border_turtle.goto(-300, 280)
        border_turtle.pendown()
        border_turtle.forward(600)
        border_turtle.hideturtle()

    def terminate_screen(self):
        self.screen.exitonclick()


class ScoreBoard(TurtleI):
    def __init__(self):
        super().__init__('white', 'arrow')
        self.score = 0
        self.hideturtle()
        self.init_pos()
        self.write_score()

    def init_pos(self):
        self.goto(0, 300 - 25)

    def write_score(self):
        self.clear()
        self.write(f'Score: {self.score}', align=TXT_ALIGN, font=TXT_STYLE)

    def up_score(self):
        self.score += 1
        self.write_score()

    def w_game_over(self):
        self.goto(0, 0)
        self.write('GAME OVER', align=TXT_ALIGN, font=TXT_STYLE)


def main():
    i_screen = ScreenI()
    i_snake = SnakeI()
    i_food = FoodI()
    i_scoreboard = ScoreBoard()

    i_screen.bind_keys(i_snake)

    game_on = True

    while game_on:
        i_screen.screen.update()
        i_snake.move()
        sleep(0.1)

        # collision with food
        if i_snake.head.distance(i_food) < 15:
            i_food.goto_rand_pos()
            i_scoreboard.up_score()
            i_snake.extend()

        # collision with wall
        if abs(i_snake.head.xcor()) > 280 or abs(i_snake.head.ycor()) > 280:
            game_on = False
            i_scoreboard.w_game_over()

        # collision with head
        for seg in i_snake.segments[1:]:
            if i_snake.head.distance(seg) < 10:
                game_on = False
                i_scoreboard.w_game_over()

    i_screen.terminate_screen()


if __name__ == '__main__':
    SC_H = 610
    SC_W = 600

    START_POS = [(0, 0), (-20, 0), (-40, 0)]
    PACE = 20
    TXT_ALIGN = 'center'
    TXT_STYLE = ('Courier', 15, 'normal')

    main()
