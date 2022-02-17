from datetime import datetime
from sre_constants import SUCCESS
import tkinter as tk
import requests
from PIL import Image, ImageTk
from KeyPad import NumbericKeyPad
from tkinter import messagebox
from State import RecognizeState
from cfg import *

BACKGROUND_PATH = "assets/images/bg_face_recognized.png"
BTN_CONFIRM_PATH = "assets/button/btn-confirm_1.png"
BTN_RETRY_PATH = "assets/button/btn.retry.png"
BTN_RETRY2_PATH = "assets/button/btn.retry (1).png"


class FaceNotMeView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='white')
        self.controller = controller
        self.master = parent

        print(datetime.now().strftime("%H:%M:%S") + ": Init FaceNotMe view ...")
        self.last_state = None
        self.current_appsize = (self.controller.winfo_width(),
                                self.controller.winfo_height())
        self.load_image()
        self.create_widgets()
        self.bind('<Configure>', self.size_change)
        self.cur_text = ""

    def load_image(self):
        self.img_left_bg = Image.open(BACKGROUND_PATH)
        with Image.open(BTN_CONFIRM_PATH).resize((130, 50)) as img:
            self.img_btn_confirm = img.copy()
            self.imgtk_btn_confirm = ImageTk.PhotoImage(img)
        with Image.open(BTN_RETRY_PATH).resize((130, 50)) as img:
            self.img_btn_retry = img.copy()
            self.imgtk_btn_retry = ImageTk.PhotoImage(img)
        with Image.open(BTN_RETRY2_PATH).resize((130, 50)) as img:
            self.img_btn_retry2 = img.copy()
            self.imgtk_btn_retry2 = ImageTk.PhotoImage(img)

    def create_widgets(self):
        self.left_frame = tk.Frame(self)
        self.left_frame.place(relx=0, rely=0, relwidth=0.33, relheight=1)
        self.left_frame_bg = tk.Label(
            self.left_frame, bd=0, highlightthickness=0, bg="black")
        self.left_frame_bg.place(relx=0, rely=0, relwidth=1,
                                 relheight=1, anchor="nw")
        self.text = tk.Label(
            self.left_frame, font=('Courier New', 22, 'bold'), background=SUCCESS_COLOR,
            fg=TEXT_WHITE_COLOR)
        self.text.place(relx=0.5, rely=0.8, anchor="center", relwidth=0.5)
        # self.btnConfirm = tk.Button(
        #     self.left_frame, bd=0, highlightthickness=0, image=self.imgtk_btn_confirm,
        #     background="#0f5d54", activebackground="#0f5d54",
        #     command=lambda: self.controller.change_state(RecognizeState.RECOGNIZED_SUCESSED))
        # self.btnConfirm.place(relx=0.5, rely=0.85, anchor="center")

        # Right Frame
        self.form_frame = tk.Frame(self, bg="white")
        self.form_frame.place(relx=0.33, rely=0, relwidth=0.67, relheight=1)
        self.input = tk.Entry(self.form_frame,
                              bd=0, justify="center", font="Helvetica 44 bold")
        self.input.place(relx=0.50, rely=0.1, anchor='center',
                         relwidth=0.50, relheight=0.05)
        self.keypad = NumbericKeyPad(self.form_frame, self)
        self.keypad.place(relx=0.50, rely=0.55, anchor="center",
                          relheight=0.8, relwidth=0.7)

    def draw_bg_left(self):
        # Get size
        w = self.current_appsize[0]
        h = self.current_appsize[1]
        w = int(w / 3)

        # Resize base background
        self.resize_img_left_bg = self.img_left_bg.resize((w, h))

        # Get Face Image from webcam
        self.img_face = self.controller.last_face

        self.img_face = self.img_face.resize((w, w))

        self.tmp_img_left_bg = Image.new("RGBA", self.resize_img_left_bg.size)
        self.tmp_img_left_bg.paste(self.img_face, (0, int(0.18 * h)))
        self.tmp_img_left_bg.paste(
            self.resize_img_left_bg, (0, 0), self.resize_img_left_bg)
        self.final_img_left_bg = ImageTk.PhotoImage(self.tmp_img_left_bg)

        self.left_frame_bg.configure(image=self.final_img_left_bg)

    def draw_keypad(self):
        h = self.current_appsize[1]
        w = self.current_appsize[0]
        w = int(w / 3)
        keypad_w = int(2 * w / 10 * 7)
        keypad_h = int(h / 10 * 8)
        self.keypad.draw(keypad_w, keypad_h)

    def size_change(self, event):
        self.current_appsize = (event.width, event.height)
        self.draw_keypad()

    def draw(self):
        self.draw_bg_left()

    def keypad_input(self, x):
        self.cur_text = self.cur_text + str(x)
        self.input.delete(0, 'end')
        self.input.insert(0, self.cur_text)

    def keypad_delete(self):
        self.input.delete(0, 'end')
        self.cur_text = self.cur_text[:-1]
        self.input.insert(0, self.cur_text)

    def show_popup(self, command: str, user_info: dict = None):
        if command == "FOUND":

            popup = tk.Frame(self.master, width=900, height=500, highlightbackground="black", highlightthickness=1,
                             bd=0,
                             bg="white")
            popup.place(relx=0.25, rely=0.2)

            # LEFT
            avatar_width, avatar_height = 250, 300
            avatar_holder = tk.Canvas(popup, width=avatar_width, height=avatar_height, highlightbackground="white",
                                      highlightthickness=1)
            avatar_holder.place(relx=0.05, rely=0.1)
            avatar_img = ImageTk.PhotoImage(
                Image.open(user_info["avatar_url"]).resize((avatar_width, avatar_height)),
                Image.ANTIALIAS)
            avatar_holder.background = avatar_img
            avatar_holder.create_image(0, 0, anchor=tk.NW, image=avatar_img)

            # ../logic/database/FACE_IMAGE/1.jpg

            # RIGHT
            form_width, form_height = 450, 400

            form_info = tk.Canvas(popup, width=form_width, height=form_height, highlightbackground="white",
                                  highlightthickness=1)
            form_info.place(relx=0.4, rely=0.1)
            form_img = ImageTk.PhotoImage(Image.open("./assets/images/Group 1.png").resize((form_width, form_height)),
                                          Image.ANTIALIAS)
            form_info.background = form_img
            form_info.create_image(0, 0, anchor=tk.NW, image=form_img)

            user_name = tk.Label(form_info, text=user_info["name"], font=('Courier New', 22, 'bold'),
                                 fg="white", bg="#127265")
            user_name.place(relx=0.2, rely=0.2)

            user_code = tk.Label(form_info, text=user_info["code"], font=('Courier New', 22, 'bold'),
                                 fg="white", bg="#127265")
            user_code.place(relx=0.38, rely=0.48)

            btn_confirm = tk.Button(form_info, bd=0, highlightthickness=0, image=self.imgtk_btn_confirm,
                                    background="#0f5d54", activebackground="#0f5d54",
                                    command=lambda: self.controller.change_state(RecognizeState.RECOGNIZED_SUCESSED))
            btn_confirm.place(relx=0.15, rely=0.75)

            btn_retry = tk.Button(form_info, bd=0, highlightthickness=0, image=self.imgtk_btn_retry2,
                                  background="#0f5d54", activebackground="#0f5d54", command=lambda: popup.destroy())
            btn_retry.place(relx=0.55, rely=0.75)

        elif command == "WARNING":
            popup = tk.Canvas(self.master, width=500, height=300, highlightbackground="white", highlightthickness=1)
            popup.place(relx=0.35, rely=0.3)
            popup_image = ImageTk.PhotoImage(Image.open("./assets/images/Group 2.png").resize((500, 300)),
                                             Image.ANTIALIAS)
            popup.background = popup_image
            popup.create_image(0, 0, anchor=tk.NW, image=popup_image)

            message = tk.Label(popup, text="CAN NOT EMPTY", font=('Courier New', 22, 'bold'),
                               fg="white", bg="#871717")
            message.place(relx=0.25, rely=0.25)
            btn_retry = tk.Button(popup, bd=0, highlightthickness=0, image=self.imgtk_btn_retry,
                                  background="#6D0A0A", activebackground="#0f5d54", command=lambda: popup.destroy())
            btn_retry.place(relx=0.37, rely=0.65)


        else:
            popup = tk.Canvas(self.master, width=500, height=300, highlightbackground="white", highlightthickness=1)
            popup.place(relx=0.35, rely=0.3)
            popup_image = ImageTk.PhotoImage(Image.open("./assets/images/Group 2.png").resize((500, 300)),
                                             Image.ANTIALIAS)
            popup.background = popup_image
            popup.create_image(0, 0, anchor=tk.NW, image=popup_image)

            message = tk.Label(popup, text="USER NOT FOUND", font=('Courier New', 22, 'bold'),
                               fg="white", bg="#871717")
            message.place(relx=0.25, rely=0.25)
            btn_retry = tk.Button(popup, bd=0, highlightthickness=0, image=self.imgtk_btn_retry,
                                  background="#6D0A0A", activebackground="#0f5d54", command=lambda: popup.destroy())
            btn_retry.place(relx=0.37, rely=0.65)

    def keypad_confirm(self):
        if len(self.cur_text) == 0:
            self.show_popup(command="WARNING")
        else:
            param = {
                'uuid_': self.cur_text
            }

            response = requests.get('http://127.0.0.1:6000/get_user', param).json()

            if response["status"] == "Found":
                self.show_popup(command="FOUND", user_info={"name": response["name"], "code": self.cur_text,
                                                            "avatar_url": response["avatar_url"]})

            else:
                self.show_popup(command="NOT FOUND")

        # self.controller.user_name = response
        # self.controller.change_state(RecognizeState.RECOGNIZED)
        self.cur_text = ""
        self.input.delete(0, 'end')
