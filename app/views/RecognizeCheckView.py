import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
from State import RecognizeState
import cv2
import requests
LEFT_BACKGROUND_PATH = "assets/images/bg_face_recognize.png"
RIGHT_BACKGROUND_PATH = "assets/images/bg_disk_recognize.png"


class RecognizeCheckView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='white')
        print(datetime.now().strftime("%H:%M:%S") +
              ": Init RecognizeCheck view ...")
        self.controller = controller
        self.current_appsize = (self.controller.winfo_screenwidth(),
                                self.controller.winfo_screenheight())
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

        # Get Face Image from webcam
        self.img_face = self.controller.frame_webcam_cap()



        # self.img_face = self.controller.last_face
        self.controller.last_face = self.img_face.copy()
        self.img_face = self.img_face.resize((w, w))

        self.tmp_img_left_bg = Image.new("RGBA", self.resize_img_left_bg.size)
        self.tmp_img_left_bg.paste(self.img_face, (0, int(0.18*h)))
        self.tmp_img_left_bg.paste(
            self.resize_img_left_bg, (0, 0), self.resize_img_left_bg)
        self.final_img_left_bg = ImageTk.PhotoImage(self.tmp_img_left_bg)

        self.left_frame_bg.configure(image=self.final_img_left_bg)
        if self.controller.RecognizeState == RecognizeState.RECOGNIZING:
            self.left_frame_bg.after(50, self.draw_bg_left)

    def draw_bg_right(self):
        # Get size
        w = self.current_appsize[0]
        h = self.current_appsize[1]
        w = int(w/3*2)+100

        # Resize base background
        self.resize_img_right_bg = self.img_right_bg.resize((w, h))

        # Get Face Image from webcam
        self.img_meal = self.controller.frame_web_cap_meal()
        # self.img_meal = self.controller.last_dish
        self.img_meal = self.img_meal.resize((int(0.80*w), int(0.60*h)))

        self.tmp_img_right_bg = Image.new(
            "RGBA", self.resize_img_right_bg.size)
        self.tmp_img_right_bg.paste(self.img_meal, (int(0.15*w), int(0.2*h)))
        self.tmp_img_right_bg.paste(
            self.resize_img_right_bg, (0, 0), self.resize_img_right_bg)
        self.final_img_right_bg = ImageTk.PhotoImage(self.tmp_img_right_bg)

        self.right_frame_bg.configure(image=self.final_img_right_bg)
        if self.controller.RecognizeState == RecognizeState.RECOGNIZING:
            self.right_frame_bg.after(50, self.draw_bg_right)
        # self.right_frame_bg.after(10, self.draw_bg_right)
