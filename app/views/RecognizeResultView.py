import tkinter as tk

import requests
from PIL import Image, ImageTk
from datetime import datetime
from State import RecognizeState
from cfg import *
from app.logic.database.run_model_service import *

LEFT_BACKGROUND_PATH = "assets/images/bg_face_recognized.png"
RIGHT_BACKGROUND_PATH = "assets/images/check_face_result_qa.png"
BTN_NOTME_PATH = "assets/button/btn-notme.png"
BTN_CONFIRM_PATH = "assets/button/btn-confirm_1.png"


class RecognizeResultView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='white')
        print(datetime.now().strftime("%H:%M:%S") +
              ": Init RecognizeResult view ...")
        self.controller = controller
        self.current_appsize = (self.controller.winfo_screenwidth(),
                                self.controller.winfo_screenheight())
        self.last_appsize = self.current_appsize
        self.load_image()
        self.create_widgets()
        self.bind('<Configure>', self.size_change)

    # Load Image
    def load_image(self):

        with Image.open(LEFT_BACKGROUND_PATH) as img:
            self.img_left_bg = img.copy()
            self.imgtk_left_bg = ImageTk.PhotoImage(img)

        with Image.open(RIGHT_BACKGROUND_PATH) as img:
            self.img_right_bg = img.copy()
            self.imgtk_right_bg = ImageTk.PhotoImage(img)

        with Image.open(BTN_NOTME_PATH) as img:
            self.img_btn_notme = img.copy()
            self.imgtk_btn_notme = ImageTk.PhotoImage(img)
        with Image.open(BTN_CONFIRM_PATH) as img:
            self.img_btn_confirm = img.copy()
            self.imgtk_btn_confirm = ImageTk.PhotoImage(img)

    # Create widgets for view
    def create_widgets(self):
        # Define Left Frame
        self.left_frame = tk.Frame(self, bd=0, bg="white")
        self.left_frame.place(relx=0, rely=0, relwidth=0.333, relheight=1)

        # Define Left Label, where we store avatar
        self.left_frame_bg = tk.Label(
            self.left_frame, bd=0, highlightthickness=0)
        self.left_frame_bg.place(
            relx=0, rely=0, relwidth=1, relheight=1, anchor="nw")

        self.btnNotMe = tk.Button(
            self.left_frame, bd=0, highlightthickness=0, image=self.imgtk_btn_notme,
            background="#0f5d54", activebackground="#0f5d54",
            command=lambda: self.controller.change_state(RecognizeState.RECONIZED_FAILED))
        self.btnNotMe.place(relx=0.17, rely=0.9, anchor="nw")
        self.btnConfirm = tk.Button(
            self.left_frame, bd=0, highlightthickness=0, image=self.imgtk_btn_confirm,
            background="#0f5d54", activebackground="#0f5d54",
            command=lambda: self.controller.change_state(RecognizeState.RECOGNIZED_SUCESSED))
        self.btnConfirm.place(relx=0.53, rely=0.9, anchor="nw")


        # self.text = tk.Label(
        #     self.left_frame, text=self.controller.user_name, font=('Courier New', 22, 'bold'), background=SUCCESS_COLOR, fg=TEXT_WHITE_COLOR)
        # self.text.place(relx=0.5, rely=0.8, anchor="center", relwidth=0.5)
        # Define Right Frame
        self.right_frame = tk.Frame(self, bg="white", bd=0)
        self.right_frame.place(relx=0.33, rely=0, relwidth=0.667, relheight=1)

        # Define Right Label, where we store disk image
        self.right_frame_bg = tk.Label(
            self.right_frame, bd=0)
        self.right_frame_bg.place(relx=0, rely=0, anchor='nw')

    # handle for window resize
    def size_change(self, event):
        self.current_appsize = (event.width, event.height)

    def draw(self):
        self.draw_bg_left()
        self.draw_bg_right()

    # Drawing for left bg
    def draw_bg_left(self):
        # Get size
        w = self.current_appsize[0]
        h = self.current_appsize[1]
        w = int(w/3)

        # Resize base background
        self.resize_img_left_bg = self.img_left_bg.resize((w, h))

        self.img_face = self.controller.last_face
        self.img_face = self.img_face.resize((w, w))

        self.tmp_img_left_bg = Image.new("RGBA", self.resize_img_left_bg.size)
        self.tmp_img_left_bg.paste(self.img_face, (0, int(0.18*h)))
        self.tmp_img_left_bg.paste(
            self.resize_img_left_bg, (0, 0), self.resize_img_left_bg)
        self.final_img_left_bg = ImageTk.PhotoImage(self.tmp_img_left_bg)

        self.left_frame_bg.configure(image=self.final_img_left_bg)

        self.text = tk.Label(
            self.left_frame, text=self.controller.user_name, font=('Courier New', 22, 'bold'), background=SUCCESS_COLOR, fg=TEXT_WHITE_COLOR)
        self.text.place(relx=0.5, rely=0.8, anchor="center", relwidth=0.5)

    def draw_bg_right(self):
        # Get size
        w = self.current_appsize[0]
        h = self.current_appsize[1]
        w = int(w/3*2)+100

        # Resize base background
        self.resize_img_right_bg = self.img_right_bg.resize((w, h))

        # Get Face Image from webcam
        self.img_dish = self.controller.last_dish
        self.img_dish = self.img_dish.resize((int(0.80*w), int(0.60*h)))

        self.tmp_img_right_bg = Image.new(
            "RGBA", self.resize_img_right_bg.size)
        self.tmp_img_right_bg.paste(self.img_dish, (int(0.15*w), int(0.2*h)))
        self.tmp_img_right_bg.paste(
            self.resize_img_right_bg, (0, 0), self.resize_img_right_bg)
        self.final_img_right_bg = ImageTk.PhotoImage(self.tmp_img_right_bg)

        self.right_frame_bg.configure(image=self.final_img_right_bg)
