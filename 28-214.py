from tkinter import Tk, Canvas, PhotoImage, Label, Button


class LabelI(Label):
    def __init__(self, txt: str, fg: str, bg: str):
        super().__init__()
        self.config(text=txt, fg=fg, bg=bg, font=(FONT_NAME, 25, 'bold'))

    def set_grid_pos(self, col, row):
        self.grid(column=col, row=row)


class ButtonI(Button):
    def __init__(self, txt, command=None):
        super().__init__()
        self.config(text=txt, highlightthickness=0, padx=5, pady=5, command=command)

    def set_grid_pos(self, row: int, col: int):
        self.grid(row=row, column=col)


class CanvasT(Canvas):
    def __init__(self, master=None):
        super().__init__()
        self.config(width=204, height=224, bg=YELLOW, highlightthickness=0)
        self.grid(column=1, row=1)

    def attach_img(self, image: PhotoImage):
        self.create_image(103, 112, image=image)

    def attach_txt(self, txt: str):
        return self.create_text(103, 130, text=txt, fill='white', font=(FONT_NAME, 25, 'bold'))


class WindowI(Tk):
    def __init__(self):
        super().__init__()
        self.title('Pomodoro')
        self.config(padx=100, pady=50, bg=YELLOW)

    def count_down(self, canvas: CanvasT, timer_txt, count):
        count_min = count // 60
        count_sec = count % 60

        canvas.itemconfig(timer_txt, text=f'{count_min:02}:{count_sec:02}')
        if count > 0:
            self.after(1000, self.count_down, canvas, timer_txt, count - 1)

    def start_timer(self, canvas: CanvasT, timer_txt):
        pass


def main():
    i_window = WindowI()
    i_canvas = CanvasT(i_window)

    t_photo = PhotoImage(file='tomato.png')
    i_canvas.attach_img(t_photo)
    timer_txt = i_canvas.attach_txt('00:00')

    label_timer = LabelI('Timer', GREEN, YELLOW)
    label_timer.set_grid_pos(1,0)

    start_btn = ButtonI('Start', command=lambda: i_window.count_down(i_canvas, timer_txt))
    start_btn.set_grid_pos(2,0)

    reset_btn = ButtonI('Reset')
    reset_btn.set_grid_pos(2,2)

    check_mark = LabelI('✔', GREEN, YELLOW)
    check_mark.set_grid_pos(1,3)

    i_window.mainloop()


if __name__ == '__main__':
    PINK = "#e2979c"
    RED = "#e7305b"
    GREEN = "#9bdeac"
    YELLOW = "#f7f5dd"
    FONT_NAME = "Courier"
    WORK_MIN = 25
    SHORT_BREAK_MIN = 5
    LONG_BREAK_MIN = 20

    main()
