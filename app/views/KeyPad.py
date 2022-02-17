from PIL import Image, ImageTk
import tkinter as tk


class KeyPadButton(tk.Button):
    def __init__(self, parent, Path, command):
        self.img = Image.open(Path)
        self.imgTk = ImageTk.PhotoImage(self.img)
        tk.Button.__init__(self, parent, image=self.imgTk,
                           command=command, bd=0, highlightthickness=0, )
        self.size = self.img.size[0]


class NumbericKeyPad(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.createBtn()

    def createBtn(self):
        self.btn1 = KeyPadButton(
            self, "assets/keypad/n1.png", command=lambda: self.controller.keypad_input(1))
        self.btn2 = KeyPadButton(
            self, "assets/keypad/n2.png", command=lambda: self.controller.keypad_input(2))
        self.btn3 = KeyPadButton(
            self, "assets/keypad/n3.png", command=lambda: self.controller.keypad_input(3))
        self.btn4 = KeyPadButton(
            self, "assets/keypad/n4.png", command=lambda: self.controller.keypad_input(4))
        self.btn5 = KeyPadButton(
            self, "assets/keypad/n5.png", command=lambda: self.controller.keypad_input(5))
        self.btn6 = KeyPadButton(
            self, "assets/keypad/n6.png", command=lambda: self.controller.keypad_input(6))
        self.btn7 = KeyPadButton(
            self, "assets/keypad/n7.png", command=lambda: self.controller.keypad_input(7))
        self.btn8 = KeyPadButton(
            self, "assets/keypad/n8.png", command=lambda: self.controller.keypad_input(8))
        self.btn9 = KeyPadButton(
            self, "assets/keypad/n9.png", command=lambda: self.controller.keypad_input(9))
        self.btn0 = KeyPadButton(
            self, "assets/keypad/n0.png", command=lambda: self.controller.keypad_input(0))
        self.btnConfirm = KeyPadButton(
            self, "assets/keypad/confirm.png", command=self.controller.keypad_confirm)
        self.btnDelete = KeyPadButton(
            self, "assets/keypad/delete.png", command=self.controller.keypad_delete)

    def draw(self, keypad_w, keypad_h):
        size = self.btn0.size
        padding_x = int((keypad_w - 3*size)/6)
        padding_y = int((keypad_h - 4*size)/8)
        self.btn1.grid(row=0, column=0, padx=padding_x, pady=padding_y)
        self.btn2.grid(row=0, column=1, padx=padding_x, pady=padding_y)
        self.btn3.grid(row=0, column=2, padx=padding_x, pady=padding_y)
        self.btn4.grid(row=1, column=0, padx=padding_x, pady=padding_y)
        self.btn5.grid(row=1, column=1, padx=padding_x, pady=padding_y)
        self.btn6.grid(row=1, column=2, padx=padding_x, pady=padding_y)
        self.btn7.grid(row=2, column=0, padx=padding_x, pady=padding_y)
        self.btn8.grid(row=2, column=1, padx=padding_x, pady=padding_y)
        self.btn9.grid(row=2, column=2, padx=padding_x, pady=padding_y)
        self.btn0.grid(row=3, column=1, padx=padding_x, pady=padding_y)
        self.btnConfirm.grid(row=3, column=2, padx=padding_x, pady=padding_y)
        self.btnDelete.grid(row=3, column=0, padx=padding_x, pady=padding_y)
