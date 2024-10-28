import logging
import os
from html import unescape
from tkinter import *
import requests
from dotenv import load_dotenv


class Question:
    def __init__(self, qs: str, ans: str):
        self.qs = unescape(qs)
        self.ans = bool(ans)


class QuizBrain:
    def __init__(self):
        logging.info(f'Initializing {self.__class__}')

        self._q_bank = self.__init_quiz_bank()
        self._score = 0
        self._cur_indx = 0

    @property
    def get_usr_score(self) -> str:
        """
        returns a string of user score and current index
        :return: str
        """

        return f'{self._score} / {self._cur_indx}'

    def __get_trivia_data(self) -> list[dict[str, str]]:
        """
        return api response
        :return: list of dict of string
        """

        url = QUIZ_URL

        api_params = {
            'amount': QUIZ_AMT,
            'category': '18',
            'type': 'boolean'
        }

        try:
            response = requests.get(url, params=api_params, timeout=TIMEOUT_MS)
            response.raise_for_status()
            resp_json = response.json().get('results', [])
            if not resp_json:
                raise ValueError("Empty Response: No data received from the API.")
            return [{'text': resp.get('question'), 'answer': resp.get('correct_answer')} for resp in
                    resp_json]
        except requests.exceptions.HTTPError as http_err:
            logging.warning(f'HTTP Error" {http_err}')
        except requests.exceptions.Timeout as time_err:
            logging.warning(f'Timeout Error: {time_err}')
        except requests.exceptions.ConnectionError as conn_err:
            logging.error(f'Connection Error: {conn_err}')
        except requests.exceptions.RequestException as req_err:
            logging.warning(f"Request Error: {req_err}")
        except ValueError as val_err:
            logging.warning(val_err)
        except Exception as e:
            logging.error(f'Unexpected Error: {e}')

        return []

    def __init_quiz_bank(self) -> list[Question]:
        """
        con api resp to a list of objects
        :return: list of Question objects
        """

        resp = self.__get_trivia_data()
        if resp:
            return [Question(q.get('text'), q.get('answer')) for q in resp]
        else:
            logging.warning('Response is empty')
            return []

    def check_ans(self, cur_ans: bool, usr_in: bool) -> bool:
        """
        compares ans,
        if equal then increments and returns true
        else false
        :return: bool
        """

        if cur_ans == usr_in:
            self._score += 1
            logging.info(f'Current Score: {self._score}')
            return True
        logging.info('User guessed incorrectly')
        return False

    def nxt_qs(self) -> Question | None:
        """
        checks if index is less than total
        if true fetches new qs and increments index then returns qs
        else returns None
        :returns: Question obj or None
        """
        if self._cur_indx < len(self._q_bank):
            cur_qs = self._q_bank[self._cur_indx]
            self._cur_indx += 1
            return cur_qs
        return None


class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        logging.info(f'Initializing {self.__class__}')

        self.backend = quiz_brain
        self.cur_q = None

        self.window = Tk()
        self.window.title('iQuiz')
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        self.score_label = Label(text='Score: 0', fg='white', bg=THEME_COLOR)
        self.score_label.grid(row=0, column=1)

        self.canvas = Canvas(width=300, height=250, bg='white')
        self.q_txt = self.canvas.create_text(150, 125,
                                             text='Some Question Text',
                                             fill=THEME_COLOR,
                                             font=('Arial', 20, 'italic'),
                                             width=280)
        self.canvas.grid(row=1, column=0, columnspan=2, pady=50)

        self.__create_ui_btn()
        self.__display_q()

    def __create_ui_btn(self):
        """
        creates ui buttons
        """

        self._cross_img = PhotoImage(file=CROSS_IMG)
        self.cross_btn = Button(image=self._cross_img,
                                highlightthickness=0,
                                command=lambda: self.__chooseAns(False))
        self.cross_btn.grid(row=2, column=0)

        self._tick_img = PhotoImage(file=TICK_IMG)
        self.tick_btn = Button(image=self._tick_img,
                               highlightthickness=0,
                               command=lambda: self.__chooseAns(True))
        self.tick_btn.grid(row=2, column=1)

    def __reset_canvas_col(self):
        """
        resets canvas and calls display_q
        """

        self.canvas.config(bg='white')
        self.__display_q()

    def __giv_feedback(self, is_correct: bool):
        """
        :params: bool
        flashes canvas according to user's ans and resets after 500 ms
        """

        color = 'green' if is_correct else 'red'
        self.canvas.config(bg=color)
        self.window.after(500, self.__reset_canvas_col)

    def __chooseAns(self, usr_ans: bool):
        """
        :params: bool
        takes user ans, fetches cur ans
        compares from backend
        gives feedback and updates label
        """

        correct_ans = self.cur_q.ans
        is_correct = self.backend.check_ans(correct_ans, usr_ans)
        self.__giv_feedback(is_correct)
        self.score_label.config(text=f'Score: {self.backend.get_usr_score}')

    def __display_q(self):
        """
        fetches next qs
        if found updates canvas
        else shows end and disables btns
        """

        self.cur_q = self.backend.nxt_qs()
        if self.cur_q:
            self.canvas.itemconfig(self.q_txt, text=self.cur_q.qs)
        else:
            self.canvas.itemconfig(self.q_txt, text='Quiz Completed')
            self.cross_btn.config(state='disabled')
            self.tick_btn.config(state='disabled')

    def run_app(self):
        self.window.mainloop()


def main():
    i_brain = QuizBrain()

    iQuizApp = QuizInterface(i_brain)
    iQuizApp.run_app()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s | %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('34-258.log')
        ]
    )

    load_dotenv()

    QUIZ_URL = os.getenv('TRIVIA_API')
    QUIZ_AMT = 10
    TIMEOUT_MS = 5000
    THEME_COLOR = '#375362'
    CROSS_IMG = '31-234_wrong.png'
    TICK_IMG = '31-234_right.png'

    main()
