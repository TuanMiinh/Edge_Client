from cProfile import label
from concurrent.futures import process
from time import sleep
import tkinter as tk
from PIL import Image, ImageTk
from StartView import StartView
from State import *
from RecognizeCheckView import RecognizeCheckView
from RecognizeResultView import RecognizeResultView
from FaceNotMeView import FaceNotMeView
from FaceFailedView import FaceFailedView
from FinishView import FinishView
from RatingView import RatingView
from RecognizeRatingResultView import RecognizeRatingResultView
import cv2
from flask import request
import requests
from threading import Thread

# Config for root view
FULLSCREEN = True
WIDTH = 1000
HEIGHT = 1000
ENVIROMENT = 'Testing'


class RootView(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.init_root_element()
        self.init_state()
        self.show_start()

    def init_root_element(self):

        # Init Container and screen
        self.title('akaCam Edge Client v2.0')
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Config root attribute
        self.attributes("-fullscreen", FULLSCREEN)
        self.geometry('{}x{}'.format(WIDTH, HEIGHT))

        # Default Face image and default Dish Image:
        with Image.open("avatar.jpg") as img:
            self.last_face = img.copy()
        with Image.open("dish.jpeg") as img:
            self.last_dish = img.copy()

        self.user_name = ""


        # Init Change view
        self.change_view = lambda: print("DeFault")

        #Init camera
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        print("Start cam 1")
        #
        self.cap2 = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        self.cap2.set(cv2.CAP_PROP_FRAME_WIDTH,1500)
        self.cap2.set(cv2.CAP_PROP_FRAME_HEIGHT,800)
        print("Start cam 2")



    def init_state(self):
        self.process_type = ProcessType.FACEFOOD
        self.RecognizeState = RecognizeState.INIT
        self.RecognizeState = RecognizeState.INIT

    def show_start(self):
        self.start_view = StartView(
            parent=self.container, controller=self)
        self.start_view.grid(row=0, column=0, sticky="nsew")

        self.start_view.tkraise()

    # Change App State:
    def change_state(self, state):
        self.RecognizeState = state
        self.change_view()

    # Change Process:

    def change_process(self, type):
        self.process_type = type
        if self.process_type == ProcessType.FACEFOOD:
            self.init_frame_facefood()
            self.change_view = self.change_view_facemeal
        if self.process_type == ProcessType.FEEDBACK:
            self.init_frame_feedback()
            self.change_view = self.change_view_feedback
        self.change_view()

    # Init frame for face food process
    def init_frame_facefood(self):

        # Init FaceMeal Recognize view
        self.recognize_view = RecognizeCheckView(
            parent=self.container, controller=self)
        self.recognize_view.grid(row=0, column=0, sticky="nsew")

        # Init FaceMeal Recognize Result view

        self.result_view = RecognizeResultView(
            parent=self.container, controller=self)
        self.result_view.grid(row=0, column=0, sticky="nsew")

        # Init FaceNotMe View:
        self.face_not_me_view = FaceNotMeView(
            parent=self.container, controller=self)
        self.face_not_me_view.grid(row=0, column=0, sticky="nsew")

        # Init FaceFail View:
        self.face_failed_view = FaceFailedView(
            parent=self.container, controller=self)
        self.face_failed_view.grid(row=0, column=0, sticky="nsew")

        # Init Finish View:
        self.finish_view = FinishView(parent=self.container, controller=self)
        self.finish_view.grid(row=0, column=0, sticky="nsew")

    def call_api(self):
        try:
            response = requests.get('http://127.0.0.1:6000/').json()["name"]
            print(response)
            self.user_name = response
        except:
            response = "CONNECTING ..."
            self.user_name = response

    # Change state for facemeal:
    def change_view_facemeal(self):
        if self.RecognizeState == RecognizeState.INIT:
            self.RecognizeState = RecognizeState.RECOGNIZING
            self.recognize_view.tkraise()
            self.recognize_view.draw()
        if self.RecognizeState == RecognizeState.RECOGNIZED:
            self.call_api()
            self.result_view.tkraise()
            self.result_view.draw()

        if self.RecognizeState == RecognizeState.UN_RECOGNIZED:
            self.face_failed_view.tkraise()
            self.face_failed_view.draw()

        if self.RecognizeState == RecognizeState.RECOGNIZED_SUCESSED:
            self.finish_view.tkraise()
            self.after(2000, lambda : self.change_state(RecognizeState.INIT))
        if self.RecognizeState == RecognizeState.RECONIZED_FAILED:
            self.face_not_me_view.tkraise()
            self.face_not_me_view.draw()
        if self.RecognizeState == RecognizeState.RETRY:
            self.RecognizeState = RecognizeState.RECOGNIZING
            self.face_failed_view.retry()



    # Init frame for feedback process:
    def init_frame_feedback(self):
        # Init FaceMeal Recognize view
        self.recognize_view = RecognizeCheckView(
            parent=self.container, controller=self)
        self.recognize_view.grid(row=0, column=0, sticky="nsew")

        # Init Rating view:
        self.rating_view = RatingView(parent=self.container, controller=self)
        self.rating_view.grid(row=0, column=0, sticky="nsew")
        # Init FeedBack Recognize Result view
        self.result_view = RecognizeRatingResultView(
            parent=self.container, controller=self)
        self.result_view.grid(row=0, column=0, sticky="nsew")

        # Init FaceNotMe View:
        self.face_not_me_view = FaceNotMeView(
            parent=self.container, controller=self)
        self.face_not_me_view.grid(row=0, column=0, sticky="nsew")

        # Init FaceFail View:
        self.face_failed_view = FaceFailedView(
            parent=self.container, controller=self)
        self.face_failed_view.grid(row=0, column=0, sticky="nsew")

        # Init Finish View:
        self.finish_view = FinishView(parent=self.container, controller=self)
        self.finish_view.grid(row=0, column=0, sticky="nsew")

    def change_view_feedback(self):
        if self.RecognizeState == RecognizeState.INIT:
            self.RecognizeState = RecognizeState.RECOGNIZING
            self.RatingState = RatingState.NOT_FINISH
            self.recognize_view.tkraise()
            self.recognize_view.draw()
        if self.RecognizeState ==  RecognizeState.RATING:
            self.rating_view.tkraise()
            self.rating_view.draw()

        if self.RecognizeState == RecognizeState.RECOGNIZED:
            self.result_view.tkraise()
            self.result_view.draw()

        if self.RecognizeState == RecognizeState.UN_RECOGNIZED:
            self.face_failed_view.tkraise()
            self.face_failed_view.draw()

        if self.RecognizeState == RecognizeState.RECOGNIZED_SUCESSED:
            self.finish_view.tkraise()

        if self.RecognizeState == RecognizeState.RECONIZED_FAILED:
            self.face_not_me_view.tkraise()
            self.face_not_me_view.draw()
        if self.RecognizeState == RecognizeState.RETRY:
            self.RecognizeState = RecognizeState.RECOGNIZING
            self.face_failed_view.retry()
        print(self.RecognizeState)

    # Send Image to frame:

    def frame_webcam_cap(self):

        _, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        self.img = Image.fromarray(cv2image).resize((600, 600))
        self.last_face = self.img.copy()
        # self.last_face.show()


        return self.img

    def frame_web_cap_meal(self):

        _, frame2 = self.cap2.read()
        frame2 = cv2.flip(frame2, 1)
        cv2image2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGBA)
        self.img2 = Image.fromarray(cv2image2).resize((600, 600))
        self.last_dish = self.img2.copy()
        # self.last_face.show()
        return self.img2

    # def start_thread(self):
    #     face_cam =  Thread(target=self.frame_webcam_cap_face)
    #     meal_cam =  Thread(target=self.frame_web_cap_meal)
    #
    #     face_cam.start()
    #     face_cam.join()
    #
    #     meal_cam.start()
    #     meal_cam.join()
    #
    #     return face_cam

    # Button for testing flow:
    def test(self):
        tk.Button(self, text="RecognizeSucessed", command=lambda: self.change_state(RecognizeState.RECOGNIZED)).place(
            relx=0, rely=0)
        tk.Button(self, text="RecognizeFail", command=lambda: self.change_state(RecognizeState.UN_RECOGNIZED)).place(
            relx=0.1, rely=0)
        tk.Button(self, text="Again", command=lambda: self.change_state(RecognizeState.INIT)).place(
            relx=0.2, rely=0)
        tk.Button(self, text="Rating", command=lambda: self.change_state(RecognizeState.RATING)).place(
            relx=0.3, rely=0)

if __name__ == '__main__':
    root = RootView()
    if ENVIROMENT == "Testing":
        root.test()
    root.mainloop()
