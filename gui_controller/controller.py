from tkinter import Tk, Label, Button, StringVar # changed the * to 'Tk, Label, Button, StringVar' because it may limit memory usage
import tkinter.font
import sys
from time import sleep

class GUIController():
    
    def __init__(self, master, name, width, height):
        self.master = master
        self.master.title( f'{name}' )
        self.master.geometry(f'{width}x{height}')

    def create_button(self, ):
        pass

class GUIButton():
    def __init__(self, master, text, method, place_x, place_y) -> None:
        self.master = master
        self.text = text
        self.method = method
        self.x = place_x
        self.y = place_y
    
    def update_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    @property
    def show(self):
        self.place(self.x, self.y)