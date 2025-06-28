import os
import logging
import random
import tkinter as tk
import time


def setup_logging(file_name: str) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(funcName)s | %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f'{file_name}.log', mode='w')
        ]
    )
    logging.info('Logging setup complete')


class TypingTestApp:
    def __init__(self, root, txt_li: list[str]):
        logging.info('Initiating app')

        self.root = root
        self.root.title("Typing Test App")
        self.txt_li = txt_li
        self.test_txt = self.init_test_txt()

        self.start_time = None
        self.timer_started = False

        # init labels
        self.label = tk.Label(root, text="Typing Speed Test", font=("Helvetica", 16, "bold"))
        self.label.pack(pady=10)

        self.text_display = tk.Label(root, text=self.test_txt, wraplength=600, font=("Helvetica", 12))
        self.text_display.pack(pady=10)

        self.entry = tk.Text(root, height=5, width=60, wrap="word", font=("Helvetica", 12))
        self.entry.pack(pady=10)
        self.entry.bind("<KeyPress>", self.start_timer)

        self.result_label = tk.Label(root, text="", font=("Helvetica", 12))
        self.result_label.pack(pady=10)

        # init buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.submit_btn = tk.Button(button_frame, text='Submit', command=self.submit_test)
        self.submit_btn.grid(row=0, column=0, padx=10)

        self.reset_btn = tk.Button(button_frame, text="Reset", command=self.reset_test)
        self.reset_btn.grid(row=0, column=1, padx=10)

        logging.info('App successfully initialized')

    def init_test_txt(self):
        """
        return a random str from txt_li
        """
        return random.choice(self.txt_li)

    def start_timer(self, event=None):
        if not self.timer_started:
            self.start_time = time.time()
            self.timer_started = True
            self.root.after(100, self.check_input)

    def check_input(self):
        typed_text = self.entry.get("1.0", tk.END).strip()
        if typed_text == self.test_txt:
            self.submit_test()
        elif self.timer_started:
            self.root.after(100, self.check_input)

    def submit_test(self):
        if not self.timer_started:
            return

        typed_text = self.entry.get("1.0", tk.END).strip()
        end_time = time.time()
        time_taken = end_time - self.start_time
        time_taken = max(time_taken, 1)

        words = len(self.test_txt.split())
        wpm = (words / time_taken) * 60
        accuracy = self.calculate_accuracy(typed_text)

        self.result_label.config(text=f"WPM: {wpm:.2f}, Accuracy: {accuracy:.2f}%")
        self.timer_started = False
        self.entry.config(state='disabled')  # prevent further input

        logging.info(f"Test completed - WPM: {wpm:.2f}, Accuracy: {accuracy:.2f}%")

    def calculate_accuracy(self, typed_text: str) -> float:
        correct = sum(1 for i, c in enumerate(typed_text) if i < len(self.test_txt) and c == self.test_txt[i])
        total = max(len(self.test_txt), 1)
        return (correct / total) * 100

    def reset_test(self):
        self.test_txt = self.init_test_txt()
        self.text_display.config(text=self.test_txt)

        self.start_time = None
        self.timer_started = False

        self.entry.config(state='normal')
        self.entry.delete("1.0", tk.END)
        self.result_label.config(text="")

        logging.info('Test reset')


def main():
    setup_logging(FILE_NAME)

    root = tk.Tk()
    app = TypingTestApp(root, TEXT_OPTIONS)
    root.mainloop()


if __name__ == "__main__":
    TEXT_OPTIONS = [
        "The quick brown fox jumps over the lazy dog.",
        "Python is a great programming language for beginners.",
        "Typing tests help improve your speed and accuracy.",
        "Always write clean and readable code.",
        "Debugging is twice as hard as writing the code in the first place."
    ]

    FILE_NAME = os.path.splitext(os.path.basename(__file__))[0]
    main()

    # TODO: Need to make this proper
