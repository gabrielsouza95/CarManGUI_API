from tkinter import Tk, Label, Button, StringVar # changed the * to 'Tk, Label, Button, StringVar' because it may limit memory usage
import tkinter.font
import sys
from time import sleep

class GUIController():
    def __init__(self, master):
        self.master = master
    
class GUIWindow(GUIController):
    def __init__(self, master, name, width, height):
        super().__init__(master=master)
        self.master = Tk()
        self.master.title( f'{name}' )
        self.master.geometry(f'{width}x{height}')
        return self.master
        
class GUIComponent(GUIController):
    def __init__(self, master, text, place_x, place_y) -> None:
        super().__init__(master=master)
        self.text = text
        self.x = place_x
        self.y = place_y

    def update_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        self.show

    @property
    def show(self):
        self.place(self.x, self.y)

class GUIButton(GUIComponent):
    def __init__(self, master, text, method, place_x, place_y) -> None:
        super().__init__(master, text, place_x, place_y)
        self.method = method
        self.instanceButton = Button(
            self.master, 
            text=f'{self.text}', 
            command=self.method
            )
        self.instanceButton.show

class GUILabel(GUIComponent):
    def __init__(self, master, text, place_x, place_y) -> None:
        super().__init__(master, text, place_x, place_y)
        self.textVar = StringVar()
        self.instanceLabel = Label(master, textvariable=self.textVar)
        self.instanceLabel.show

    def update_text(self, new_text): 
        self.textVar.set(f'{new_text}')
        self.instanceLabel.show
    
