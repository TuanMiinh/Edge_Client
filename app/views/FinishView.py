from cgitb import text
from datetime import datetime
import tkinter as tk
from PIL import Image, ImageTk
from State import RecognizeState
# Config Image Path
LOGO_PATH = 'assets/images/LOGO.png'
FOOTER_PATH = 'assets/images/startview_footer.png'


class FinishView(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="white")
        print(datetime.now().strftime("%H:%M:%S") + ": Init Finish view ...")
        self.controller = controller
        self.load_img()
        self.create_widgets()


    def load_img(self):
        # logo
        with Image.open(LOGO_PATH) as img:
            self.img_Logo = img.copy()
            self.imgtk_Logo = ImageTk.PhotoImage(img)
        # fotter:
        with Image.open(FOOTER_PATH) as img:
            self.img_startview_footer = img.copy()
            self.imgtk_startview_footer = ImageTk.PhotoImage(img)

    def create_widgets(self):
        # logo
        logo = tk.Label(self, image=self.imgtk_Logo, bg='White')
        logo.place(relx=0, rely=0.2, relwidth=1)

        # footer
        self.footer = tk.Label(
            self, image=self.imgtk_startview_footer, bg='White')
        self.footer.place(relx=0, rely=0.78, relwidth=1, relheight=0.25)
        self.footer.bind('<Configure>', self._resize_footer)

        # Text
        self.text = tk.Label(self, text="THANK YOU", bg="white")
        self.text.place(relx=0, rely=0.5, relwidth=1)

    def _resize_footer(self, event):
        new_width = event.width
        new_height = event.height
        new_footer = self.img_startview_footer.resize((new_width, new_height))
        self.imgtk_startview_footer = ImageTk.PhotoImage(new_footer)
        self.footer.configure(image=self.imgtk_startview_footer)
