import secrets

import pyperclip
import ttkbootstrap as ttk
import string
from dataclasses import dataclass


@dataclass
class PasswordGenerator:

    def __init__(self):
        self.root = ttk.Window(themename='superhero')
        self.root.geometry("512x384")
        self.root.resizable(False, False)
        self.root.title("Password Generator")

        self.size_var = ttk.IntVar(value=15)
        self.count_var = ttk.IntVar(value=0)
        self.password_var = ttk.StringVar(value='')
        self.password_var.trace_add('write', self.on_password_change)
        self.info_var = ttk.StringVar(value='No Password ...')

        self.style = ttk.Style()
        self.update_font_size()
        self.root.bind("<Control-equal>", self.increase_font_size)
        self.root.bind("<Control-minus>", self.decrease_font_size)

        frame = ttk.Frame(self.root, padding='10')

        self.count_label = ttk.Label(frame, textvariable=self.count_var, anchor='e')
        self.password_label = ttk.Label(frame, textvariable=self.info_var)
        self.password_entry = ttk.Entry(frame, textvariable=self.password_var, width=20)
        self.generate_button = ttk.Button(frame, text="Generate Password", bootstyle='success')

        self.password_length_spinbox = ttk.Spinbox(frame, from_=8, to=32)
        self.password_length_spinbox.set(8)

        self.copy_button = ttk.Button(frame, text="Copy", bootstyle='info')

        self.punctuation_var = ttk.BooleanVar(self.root, value=True)
        self.punctuation_check = ttk.Checkbutton(frame, text=f'{string.punctuation}',
                                                 variable=self.punctuation_var,
                                                 onvalue=True, offvalue=False)

        secrets.choice(string.ascii_letters + string.digits + string.punctuation)

        frame.place(relwidth=1, relheight=1)

        self.password_label.place(relwidth=1, y=0)
        #########################################################################
        self.password_entry.place(relwidth=0.90, y=30)
        self.count_label.place(relwidth=0.10, y=30, relx=1, anchor='ne')
        #########################################################################
        self.generate_button.place(relwidth=.85, y=70)
        self.copy_button.place(relwidth=.25, y=70, relx=1, anchor='ne')
        #########################################################################
        self.password_length_spinbox.place(width=75, y=135, relx=1, anchor='ne')
        self.punctuation_check.place(relwidth=.6, y=135)

        self.password_length = 8
        self.remembered_password = ''
        self.generate_button.config(command=self.generate_password)
        self.copy_button.config(command=self.copy_password)
        self.password_length_spinbox.config(command=self.update_password_length)

    def run(self):
        self.root.mainloop()

    def on_password_change(self, *_):
        password = self.password_var.get()
        length = len(password)
        index = self.password_entry.index('insert') - 1
        print(index)
        if length > 32:
            self.info_var.set('Reached max password length 32!')
            self.password_var.set(password[:index] + password[index + 1:])
            self.password_entry.config(bootstyle='danger')
            return
        self.password_entry.config(bootstyle='default')
        self.count_var.set(self.count_var.get() + 1)
        self.info_var.set(f'Password({length}) edited.')

    def update_password_length(self):
        self.info_var.set(f'New Password Length: {self.password_length_spinbox.get()}')

    def generate_password(self):
        self.count_var.set(self.count_var.get() + 1)
        length = int(self.password_length_spinbox.get())
        self.info_var.set(f'Password({self.password_length_spinbox.get()}) generated!')
        punctuations = ''
        if self.punctuation_var.get():
            punctuations = string.punctuation
        password = ''.join(
            secrets.choice(string.ascii_letters + string.digits + punctuations)
            for _ in range(length)
        )
        self.password_var.set(password)
        # self.password_label.config(bootstyle='success')
        # self.password_entry.config(bootstyle='success')

    def copy_password(self):
        pyperclip.copy(self.password_var.get())
        self.info_var.set(f'Password({len(self.password_var.get())}) copied!')

    def update_font_size(self):
        font = ('Monofonto', self.size_var.get())
        self.style.configure("TLabel", font=font)
        self.style.configure("TButton", font=font)
        self.style.configure("TCheckbutton", font=font)
        self.style.configure("TRadiobutton", font=font)
        self.style.configure("TEntry", font=font)
        if hasattr(self, 'password_entry'):
            self.password_entry.config(font=font)
        self.style.configure("TSpinbox", font=font)

    def increase_font_size(self, _):
        self.size_var.set(self.size_var.get() + 1)
        self.update_font_size()

    def decrease_font_size(self, _):
        self.size_var.set(self.size_var.get() - 1)
        self.update_font_size()


if __name__ == "__main__":
    app = PasswordGenerator()
    app.run()
