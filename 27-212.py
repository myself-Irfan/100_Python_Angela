from tkinter import Tk, Entry, Button, Label


class LabelI(Label):
    def __init__(self, txt: str | int):
        super().__init__()
        self.config(text=txt)

    def set_grid_pos(self, col: int, row: int):
        self.grid(column=col, row=row)

    def up_txt(self, txt: int | float):
        self.config(text=txt)
        

class EntryI(Entry):
    def __init__(self):
        super().__init__()

    def set_grid_pos(self, col: int, row: int):
        self.grid(column=col, row=row)

    def return_in(self):
        return float(self.get())
        

class ButtonI(Button):
    def __init__(self, txt: str, entry: EntryI, label: LabelI):
        super().__init__()
        self.config(text=txt, command=lambda: self.click_action(entry, label))

    def set_grid_pos(self, col: int, row: int):
        self.grid(column=col, row=row)

    def click_action(self, entry: EntryI, label: LabelI):
        usr_in = entry.return_in()
        km = miles_to_km(usr_in)
        label.up_txt(km)


class WindowI(Tk):
    def __init__(self):
        super().__init__()
        self.title('Miles to KM')
        self.minsize(width=100, height=100)
        self.config(padx=10, pady=10)


def miles_to_km(miles: float) -> float:
    try:
        return miles * 1.609
    except ValueError:
        return 0.0


def main():
    i_window = WindowI()

    miles_label = LabelI('Miles')
    miles_label.set_grid_pos(2, 0)

    is_equal = LabelI('is equal to')
    is_equal.set_grid_pos(0,1)

    km_result = LabelI(0)
    km_result.set_grid_pos(1,1)

    km_label = LabelI('Km')
    km_label.set_grid_pos(2,1)
    
    miles_in = EntryI()
    miles_in.set_grid_pos(1, 0)

    calculate_btn = ButtonI('Calculate', miles_in, km_result)
    calculate_btn.set_grid_pos(1, 2)

    i_window.mainloop()


if __name__ == '__main__':
    main()