from tkinter import Tk, Canvas, PhotoImage, Label, Button, messagebox
import pandas as pd
from pandas.errors import EmptyDataError
import random


class FlashCardApp:
    def __init__(self, backend):
        self.backend = backend
        self.cur_wrd = {}
        self.flip_timer = None

        self.window = Tk()
        self.window.title('iFlash')
        self.window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

        self.__create_cardboard()
        self.__next_card()
        self.__create_ui_btn()

    def __create_cardboard(self):
        self.canvas = Canvas(width=800, height=526)
        self.card_front_img = PhotoImage(file="31-234_card_front.png")
        self.card_back_img = PhotoImage(file='31-234_card_back.png')
        self.card_bg = self.canvas.create_image(400, 263, image=self.card_front_img)
        self.canvas.grid(row=0, column=0, columnspan=2)
        self.canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)

        self.title_txt = self.canvas.create_text(400, 150, text='', font=('Arial', 40, "italic"))
        self.word_txt = self.canvas.create_text(400, 263, text='', font=('Arial', 60, 'bold'))

    def __create_ui_btn(self, cross_path='31-234_wrong.png', tick_path='31-234_right.png'):
        self.cross_img = PhotoImage(file=cross_path)
        self.tick_img = PhotoImage(file=tick_path)

        self.unknown_btn = Button(image=self.cross_img, highlightthickness=0, command=self.__next_card)
        self.unknown_btn.grid(row=1, column=0)

        self.check_btn = Button(image=self.tick_img, highlightthickness=0, command=self.__rm_nxt_card)
        self.check_btn.grid(row=1, column=1)

    def __next_card(self):
        if self.flip_timer:
            self.window.after_cancel(self.flip_timer)

        try:
            self.flip_timer = 0
            self.cur_wrd = self.backend.gen_rand_word()
            self.canvas.itemconfig(self.title_txt, text='French', fill='black')
            self.canvas.itemconfig(self.word_txt, text=self.cur_wrd['French'].title(), fill='black')
            self.canvas.itemconfig(self.card_bg, image=self.card_front_img)
            self.flip_timer = self.window.after(FLIP_MS, func=self.__flip_card)
        except IndexError as e:
            messagebox.showerror('Warning', f'No words available {e}')
        except KeyError as e:
            messagebox.showerror('Error', f'Missing required keys: {e}')
        except Exception as e:
            messagebox.showerror('Error', f'Failed to fetch next word due to {e}')

    def __rm_nxt_card(self):
        self.backend.rm_wrd(self.cur_wrd)
        self.__next_card()

    def __flip_card(self):
        self.canvas.itemconfig(self.title_txt, text='English', fill='white')
        self.canvas.itemconfig(self.word_txt, text=self.cur_wrd['English'].title(), fill='white')

        self.canvas.itemconfig(self.card_bg, image=self.card_back_img)

    def run_app(self):
        self.window.mainloop()

class FlashCardB:
    def __init__(self, csv_path):
        self.data = self.__get_csv_data(csv_path)

    def __get_csv_data(self, csv_path) -> list[dict]:
        try:
            df = pd.read_csv(csv_path, dtype=str)
        except EmptyDataError as e:
            raise EmptyDataError(f'{csv_path} is empty | {e}')
        except FileNotFoundError as e:
            raise FileNotFoundError(f'{csv_path} not found | {e}')
        else:
            print(f'Data size -> {df.shape}')
            return df.to_dict(orient='records')

    def gen_rand_word(self):
        return random.choice(self.data)

    def rm_wrd(self, wrd_to_rm: dict):
        self.data = [word for word in self.data if word != wrd_to_rm]
        print(f'Removed {wrd_to_rm} | Remaining -> {len(self.data)}')

def main():
    i_backend = FlashCardB(CSV_PATH)

    i_app = FlashCardApp(i_backend)
    i_app.run_app()


if __name__ == '__main__':
    BACKGROUND_COLOR = '#B1DDC6'
    CSV_PATH = '31-234_fr_wrd.csv'
    FLIP_MS = 3000

    main()