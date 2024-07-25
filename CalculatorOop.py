import customtkinter as ctk
from tkinter import ttk
from MainCalculator import CalculatorFrame
from CurrencyConverter import ConverterFrame
from SideBar import SideBar

# APP CLASS
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry('800x700')
        self.title('Calculator')
        self.iconbitmap('Calculator.ico')
        self.minsize(width= 250, height= 400)

        self.frame = Frame(self)   
        self.side_bar = SideBar(self)

        self.mainloop()
    
    def SideScroll(self):
        self.side_bar.Animate()

class Frame():
    def __init__(self,window):
        self.id = 0
        self.window = window
        self.calculator_frame = CalculatorFrame(window)
        self.active_frame = self.calculator_frame

    def CalculatorSwitch(self):
        if self.id != 0:
            self.active_frame.pack_forget()
            self.active_frame.destroy()
            self.active_frame = CalculatorFrame(self.window)
            self.active_frame.lower()
            self.id = 0

    def ConverterSwitch(self):
        if self.id != 1:
            self.active_frame.pack_forget()
            self.active_frame.destroy()
            self.active_frame = ConverterFrame(self.window)
            self.active_frame.lower()
            self.id = 1

app = App()