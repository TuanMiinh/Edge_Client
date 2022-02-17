import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
from State import ProcessType
# Config Image Path
LOGO_PATH = 'assets/images/LOGO.png'
FOOTER_PATH = 'assets/images/startview_footer.png'
FACEMEAL_BTN_PATH = 'assets/button/btn_face_meal.png'
FEEDBACK_BTN_PATH = 'assets/button/btn_feedback.png'


class StartView(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="white")
        self.controller = controller
        print(datetime.now().strftime("%H:%M:%S") + ": Init start view ...")
        self.load_image()
        self.create_widgets()

        self.current_appsize = (0, 0)
        self.bind('<Configure>', self.size_change)

    # Load Image and convert to ImageTK format
    def load_image(self):

        # Load logo
        with Image.open(LOGO_PATH) as img:
            self.img_Logo = img.copy()
            self.imgtk_Logo = ImageTk.PhotoImage(img)

        # Load Footer
        with Image.open(FOOTER_PATH) as img:
            self.img_footer = img.copy()
            self.imgtk_startview_footer = ImageTk.PhotoImage(img)

        # Load Face-Meal Button
        with Image.open(FACEMEAL_BTN_PATH) as img:
            self.img_btn_face_meal = img.copy()
            self.imgtk_btn_face_meal = ImageTk.PhotoImage(img)

        # Load FeedBack Button
        with Image.open(FEEDBACK_BTN_PATH) as img:
            self.img_btn_feedback = img.copy()
            self.imgtk_btn_feedback = ImageTk.PhotoImage(img)

    # Create and place widgets
    def create_widgets(self):
        # Logo Label
        self.logo = tk.Label(self, image=self.imgtk_Logo, bg='White')
        self.logo.place(relx=0, rely=0.2, relwidth=1)

        # Footer Label
        self.footer = tk.Label(
            self, image=self.imgtk_startview_footer, bg='White')
        self.footer.place(relx=0, rely=0.78, relwidth=1, relheight=0.25)
        # self.bind('<Configure>', self._resize_footer)
        # Face-Meal button
        self.btn_face_meal = tk.Button(
            self, image=self.imgtk_btn_face_meal,
            bg='white', activebackground='white',
            highlightthickness=0, bd=0,
            command=lambda: self.controller.change_process(ProcessType.FACEFOOD))
        self.btn_face_meal.place(relx=0.4, rely=0.5, anchor='center')

        # FeedBack button
        self.btn_feedback = tk.Button(
            self, image=self.imgtk_btn_feedback,
            bg='white', activebackground='white',
            highlightthickness=0, bd=0,
            command=lambda: self.controller.change_process(ProcessType.FEEDBACK))

        self.btn_feedback.place(relx=0.6, rely=0.5, anchor='center')
    # Get current appsize

    def get_current_size(self):
        return (self.current_appsize[0], self.current_appsize[1])
    # Responsive Image Handler

    def size_change(self, event):
        self.current_appsize = (event.width, event.height)
        self.change_size_footer()

    def change_size_footer(self):
        new_width, new_height = self.get_current_size()
        new_footer = self.img_footer.resize((new_width, int(new_height/4)))
        self.imgtk_startview_footer = ImageTk.PhotoImage(new_footer)
        self.footer.configure(image=self.imgtk_startview_footer)
