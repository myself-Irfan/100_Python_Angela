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
        self.cycle = 0
        self.check_li = ''
        self.timer_id = None

    def count_down(self, canvas: CanvasT, label_timer: LabelI, timer_txt, count, check_mark):
        count_min = count // 60
        count_sec = count % 60

        canvas.itemconfig(timer_txt, text=f'{count_min:02}:{count_sec:02}')
        if count > 0:
            self.timer_id = self.after(1000, self.count_down, canvas, label_timer, timer_txt, count - 1, check_mark)
        else:
            if self.cycle < 8:
                self.start_timer(canvas, label_timer, timer_txt, check_mark)
                if self.cycle % 2 == 0:
                    self.check_li += '✔'
                    check_mark.config(text=self.check_li)

    def start_timer(self, canvas: CanvasT, label_timer: LabelI, timer_txt, check_mark):
        self.cycle += 1

        if self.cycle == 8:
            label_timer.config(text='BREAK', fg=RED)
            self.count_down(canvas, label_timer, timer_txt, LONG_BREAK_MIN, check_mark)
        elif self.cycle % 2 == 0:
            label_timer.config(text='BREAK', fg=PINK)
            self.count_down(canvas, label_timer, timer_txt, SHORT_BREAK_MIN, check_mark)
        else:
            label_timer.config(text='WORK', fg=GREEN)
            self.count_down(canvas, label_timer, timer_txt, WORK_MIN, check_mark)

    def reset_timer(self, canvas, timer_txt, label, check_mark):
        self.cycle = 0
        self.check_li = ''
        check_mark.config(text=self.check_li)
        if self.timer_id:
            self.after_cancel(self.timer_id)
        canvas.itemconfig(timer_txt, text='00:00')
        label.config(text='TIMER', fg=GREEN)


def main():
    i_window = WindowI()
    i_canvas = CanvasT(i_window)

    t_photo = PhotoImage(file='tomato.png')
    i_canvas.attach_img(t_photo)
    timer_txt = i_canvas.attach_txt('00:00')

    label_timer = LabelI('TIMER', GREEN, YELLOW)
    label_timer.set_grid_pos(1,0)

    check_mark = LabelI('', GREEN, YELLOW)
    check_mark.set_grid_pos(1,3)

    start_btn = ButtonI('Start', command=lambda: i_window.start_timer(i_canvas, label_timer, timer_txt, check_mark))
    start_btn.set_grid_pos(2,0)

    reset_btn = ButtonI('Reset', command=lambda: i_window.reset_timer(i_canvas, timer_txt, label_timer, check_mark))
    reset_btn.set_grid_pos(2,2)

    i_window.mainloop()


if __name__ == '__main__':
    PINK = "#e2979c"
    RED = "#e7305b"
    GREEN = "#9bdeac"
    YELLOW = "#f7f5dd"
    FONT_NAME = "Courier"
    WORK_MIN = 15
    SHORT_BREAK_MIN = 5
    LONG_BREAK_MIN = 10

    main()
