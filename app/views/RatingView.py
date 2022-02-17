from distutils import command
from email.mime import image
import tkinter as tk
from PIL import Image, ImageTk
from KeyPad import NumbericKeyPad
from tkinter import PhotoImage, messagebox

LEFT_BACKGROUND_PATH = "assets/images/bg_face_recognize.png"
FORM_BACKGROUND_PATH = "assets/images/RatingPage_noBtn.png"
STAR_PATH = "assets/images/star.png"
UNSTAR_PATH = "assets/images/unstar.png"


class RatingView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='white')
        self.controller = controller
        self.master = parent
        print("Init Rating view: " + str(self.controller.winfo_width()) +
              " " + str(self.controller.winfo_height()))
        self.last_state = None
        self.cur_appsize = (self.controller.winfo_width(),
                            self.controller.winfo_height())
        self.load_image()
        self.create_widgets()
        self.bind('<Configure>', self.size_change)
        self.cur_text = ""

    def load_image(self):
        self.img_left_bg = Image.open(LEFT_BACKGROUND_PATH)
        self.form_frame_bg_img = Image.open(FORM_BACKGROUND_PATH)
        self.star_img = Image.open(STAR_PATH)
        self.unstar_img = Image.open(UNSTAR_PATH)

    def create_widgets(self):
        self.left_frame = tk.Frame(self, bd=0)
        self.left_frame.place(relx=0, rely=0, relwidth=0.33, relheight=1)
        self.left_frame_bg = tk.Label(
            self.left_frame, bd=0, highlightthickness=0, bg="white")
        self.left_frame_bg.place(relx=0, rely=0, relwidth=1,
                                 relheight=1, anchor="nw")

        # Define Right Frame
        self.form_frame = tk.Frame(self, bg="white", bd=0)
        self.form_frame.place(relx=0.33, rely=0, relwidth=0.667, relheight=1)

        # Define Right Label, where we store disk image

    def draw_bg_left(self):
        h = self.cur_appsize[1]
        w = self.cur_appsize[0]
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



    def draw_bg_right(self):
        w = int(self.cur_appsize[0] / 3 * 2)
        h = self.cur_appsize[1]
        w_new = int(w / 1024 * self.star_img.size[0]/2)
        h_new = int(h / 1050 * self.star_img.size[1]/2)

        self.form_frame_bg_img = self.form_frame_bg_img.resize(
            (int(w)+10, h))
        self.form_frame_bg_imgtk = ImageTk.PhotoImage(self.form_frame_bg_img)
        self.form_frame_bg = tk.Label(
            self.form_frame, image=self.form_frame_bg_imgtk, bg='white', bd=0)
        self.form_frame_bg.place(relx=0, rely=0, anchor='nw')

        self.unstar_img_copy = self.unstar_img.resize((w_new, h_new))
        self.unstar_imgtk = ImageTk.PhotoImage(self.unstar_img_copy)

        self.star_img_copy = self.star_img.resize((w_new, h_new))
        self.star_imgtk = ImageTk.PhotoImage(self.star_img_copy)

        self.rating_frame = tk.Frame(
            self.form_frame, bg='white')
        self.rating_frame.place(
            relx=0.5, rely=0.62, anchor='center', relheight=0.142, relwidth=0.63)
        self.stars = []
        x = 1
        for i in range(5):
            self.stars.append(tk.Button(self.rating_frame, image=self.unstar_imgtk,
                                        bg='white', activebackground='white', highlightthickness=0, bd=0))
            self.stars[i].place(relx=i*0.2+0.1, rely=0.5, anchor='center')
        self.stars[0].config(command=lambda: self.rating(0))
        self.stars[1].config(command=lambda: self.rating(1))
        self.stars[2].config(command=lambda: self.rating(2))
        self.stars[3].config(command=lambda: self.rating(3))
        self.stars[4].config(command=lambda: self.rating(4))






    def rating(self, x):
        self.stars[1].config(image=self.star_imgtk)
        for btn in self.stars:
            btn.config(image=self.unstar_imgtk)
        for i in range(x+1):
            self.stars[i].config(image=self.star_imgtk)

    def size_change(self, event):
        self.cur_appsize = (event.width, event.height)

    def draw(self):
        self.draw_bg_left()
        self.draw_bg_right()
