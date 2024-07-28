import collections
import re
import secrets

import pyperclip
import ttkbootstrap as ttk
import string
from dataclasses import dataclass


@dataclass
class PasswordGenerator:
    magic_word_map = {
        'a': '@',
        'e': '3',
        'i': '1',
        'o': '0',
        's': '$',
        't': '7',
        'l': '1',
        'z': '2',
        'A': '@',
        'E': '3',
        'I': '1',
        'O': '0',
        'S': '$',
        'T': '7',
        'L': '1',
        'Z': '2'
    }

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
        self.root.bind("<Control-z>", self.go_back_in_history)
        self.root.bind("<Control-Z>", self.go_forward_in_history)

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
        self.magic_word_var = ttk.BooleanVar(self.root, value=False)
        self.magic_word_check = ttk.Checkbutton(frame, text='Magic Word',
                                                variable=self.magic_word_var,
                                                state='disabled',
                                                onvalue=True, offvalue=False)
        self.magic_restore_button = ttk.Button(frame, text="Restore", bootstyle='danger', state='disabled')

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
        self.punctuation_check.place(relwidth=.8, y=135)
        self.magic_word_check.place(relwidth=.6, y=170)
        self.magic_restore_button.place(relwidth=.2, y=170, x=140)

        self.password_length = 8
        self.remembered_password = ''
        self.magic_using = False
        self.history_skip = False
        self.history = []
        self.history_index = -1
        self.generate_button.config(command=self.generate_password)
        self.copy_button.config(command=self.copy_password)
        self.password_length_spinbox.config(command=self.update_password_length)
        self.magic_word_check.config(command=self.on_around_word_change)
        self.magic_restore_button.config(command=self.on_magic_restore_pressed)

    def on_around_word_change(self):
        if self.magic_word_var.get():
            self.remembered_password = self.password_var.get()
            self.password_length_spinbox.config(state='disabled')
            self.magic_restore_button.config(state='active')
            return
        self.remembered_password = ''

    def run(self):
        self.root.mainloop()

    def on_magic_restore_pressed(self):
        self.password_var.set(self.remembered_password)
        self.magic_word_var.set(False)
        self.magic_word_check.config(state='disabled')
        self.magic_using = False
        self.password_length_spinbox.config(state='active')
        self.magic_restore_button.config(state='disabled')

    def on_password_change(self, *_):
        password = self.password_var.get()
        if self.history_skip:
            self.history_skip = False
        else:
            self.add_to_history(password)
        length = len(password)
        index = self.password_entry.index('insert') - 1
        if len(re.sub(r'[^a-zA-Z]', '', password)) < 4 or length < 8:
            self.magic_word_var.set(False)
            self.magic_word_check.config(state='disabled')
            self.magic_using = False
            self.password_length_spinbox.config(state='active')
            self.magic_restore_button.config(state='disabled')
            return
        self.magic_word_check.config(state='active')
        if length > 32:
            self.info_var.set('Reached max password length 32!')
            self.password_var.set(password[:index] + password[index + 1:])
            self.password_entry.config(bootstyle='danger')
            return
        if self.magic_word_var.get() and not self.magic_using:
            self.remembered_password = password
        self.password_entry.config(bootstyle='default')
        self.count_var.set(self.count_var.get() + 1)
        self.info_var.set(f'Password({length}) edited.')

    def update_password_length(self):
        self.info_var.set(f'New Password Length: {self.password_length_spinbox.get()}')

    def generate_password(self):
        def get_random_character(exclude=''):
            s = string.ascii_letters + string.digits + punctuations
            for it in exclude:
                s = s.replace(it, '')
            return secrets.choice(s)

        length = int(self.password_length_spinbox.get())
        punctuations = ''
        if self.punctuation_var.get():
            punctuations = string.punctuation
        if self.magic_word_var.get():
            self.magic_using = True
            new_password = re.sub(r'[^a-zA-Z]', '$', self.remembered_password)
            unique = list(set(self.remembered_password.replace('$', '')))
            while '$' in new_password:
                new_password = new_password.replace('$', get_random_character(exclude=string.ascii_letters), 1)
            for _ in range(len(unique) // 2):
                if len(unique) == 0:
                    break
                if secrets.randbelow(2):
                    character = secrets.choice(unique)
                    unique.remove(character)
                    new_character = self.__class__.magic_word_map.get(character.lower(), character)
                    new_password = new_password.replace(character, new_character, 1)
        else:
            new_password = ''.join(get_random_character() for _ in range(length))
        self.info_var.set(f'Password({self.password_length_spinbox.get()}) generated!')
        self.password_var.set(new_password)
        self.count_var.set(self.count_var.get() + 1)

    def add_to_history(self, value):
        self.history_index += 1
        if self.history_index < len(self.history):
            self.history[:] = self.history[:self.history_index]
        self.history.insert(self.history_index, value)

    def go_back_in_history(self, _):
        if len(self.history) == 0:
            self.history_index = -1
            return
        if self.history_index - 1 < 0:
            self.history_index = 0
            return
        self.history_index -= 1
        self.history_skip = True
        self.password_var.set(self.history[self.history_index])

    def go_forward_in_history(self, _):
        if self.history_index + 1 >= len(self.history):
            self.history_index = len(self.history) - 1
            return
        self.history_index += 1
        self.history_skip = True
        self.password_var.set(self.history[self.history_index])

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
