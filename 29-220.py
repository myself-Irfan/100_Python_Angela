from tkinter import Tk, Canvas, PhotoImage, Label, Entry, Button, END, messagebox
from pwd_gen import gen_pwd # 5_57 need to be renamed to import
import pyperclip
import json


class PwdManageApp:
    def __init__(self):
        self.window = Tk()
        self.window.title('iPassGen')
        self.window.config(padx=50, pady=50)

        # init logo
        self.create_logo()

        # init label
        self.create_label('Website', 1)
        self.create_label('E-mail/Username', 2)
        self.create_label('Password', 3)

        # init entry
        self.e_website = self.create_entry(1)
        self.e_usrmail = self.create_entry(2)
        self.e_pwd = self.create_entry(3, 18, 1)

        # init btn
        self.create_btn('Generate Password', self.gen_pwd, 3, 2)
        self.create_btn('Add Credentials', self.save_creds, 4, 1, colspan=2, width=36)

    def create_logo(self):
        self.canvas = Canvas(height=200, width=200)
        self.logo_img = PhotoImage(file='29-220.png')
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.grid(row=0, column=1)

    def create_label(self, txt, row):
        label = Label(text=txt)
        label.grid(row=row, column=0, sticky='e')

    def create_entry(self, row, width=35, colspan=2):
        entry = Entry(width=width)
        entry.grid(row=row, column=1, columnspan=colspan, sticky='w')

        return entry

    def empty_entry(self):
        self.e_website.delete(0, END)
        self.e_usrmail.delete(0, END)
        self.e_pwd.delete(0, END)

    def create_btn(self, txt, cmd, row, col, colspan=1, width=None):
        btn = Button(text=txt, command=cmd)
        if width:
            btn.config(width=width)
        btn.grid(row=row, column=col, columnspan=colspan, sticky='w')

    def gen_pwd(self):
        rand_gen_pwd = gen_pwd()
        pyperclip.copy(rand_gen_pwd)
        self.e_pwd.delete(0, END)
        self.e_pwd.insert(0, rand_gen_pwd)

    def save_creds(self):
        usr_web = self.e_website.get()
        usr_info = self.e_usrmail.get()
        usr_pwd = self.e_pwd.get()

        new_entry = {
            f"{usr_web}": {
                "email": usr_info,
                "password": usr_pwd
            }
        }

        if usr_pwd and usr_info and usr_web:
            if messagebox.askokcancel(title=f"{usr_web}", message=f"Confirm save:\n Username/E-mail: {usr_info}\n Password: {usr_pwd}"):
                with open('29-220.json', 'a') as f:
                    json.dump(new_entry, f)
                self.empty_entry()
        else:
            messagebox.showerror(title='ERROR', message=f'Please fill the empty field')

    def run_app(self):
        self.window.mainloop()


if __name__ == '__main__':
    i_app = PwdManageApp()
    i_app.run_app()
