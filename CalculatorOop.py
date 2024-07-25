import customtkinter as ctk
from MainCalculator import CalculatorFrame

# APP CLASS
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry('500x700')
        self.title('Calculator')
        self.iconbitmap('Calculator.ico')
 
        self.calculator_frame = CalculatorFrame(self)
        self.side_bar = SideBar(self)   

        self.mainloop()
    
    def SideScroll(self):
        self.side_bar.Animate()

class SideBar(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)

        self.parent = parent
        self.configure(fg_color = 'transparent', width = 225)
        self.start_pos = -225
        self.end_pos = 0

        self.pos = self.start_pos
        self.in_start_pos = True
        self.is_animating = False

        self.place(x = self.start_pos,rely= 0,relheight = 1,anchor = 'nw')

        self.front_button = ctk.CTkButton(
            parent,
            text_color = 'white', 
            hover = False,
            command = parent.SideScroll, 
            fg_color='transparent', 
            text= "///", 
            hover_color= '#424242', 
            width= 40,
            font= ('Arial', 22))
        
        self.SideButton = ctk.CTkButton(
            self,
            text_color = 'white', 
            command = parent.SideScroll, 
            fg_color='transparent', 
            text= "///", 
            hover_color= '#424242', 
            width= 40,
            font= ('Arial', 22))
        
        self.calculator_button = ctk.CTkButton(
            self,
            text_color = 'white',
            fg_color= 'transparent',
            text= "Calculator", 
            hover_color= '#424242',
            height = 50, 
            font= ('Arial', 22))
        self.calculator_button.place(y = 70,relx = 0.5,relwidth = 1, anchor = 'center')
        
        self.PlaceButton()
    
    def Animate(self):
        if self.is_animating == False:
            if self.in_start_pos:
                self.SideButton.place_forget()
                self.animate_forward()
            else:
                self.SideButton.place_forget()
                self.animate_backwards()
            self.is_animating = True

    def animate_forward(self):
        if self.pos < self.end_pos:
            if self.pos + 20 > self.end_pos:
                self.pos = self.end_pos
            else:
                self.pos += 20
            self.place(x = self.pos, rely= 0, relheight = 1,anchor = 'nw')
            self.front_button.place(x = 10,y= 10, anchor = 'nw')
            self.after(10, self.animate_forward)
        else:
            self.in_start_pos = False
            self.is_animating = False
            self.front_button.place_forget()
            self.PlaceButton()

    def animate_backwards(self):
        if self.pos > self.start_pos:
            if self.pos - 20 < self.start_pos:
                self.pos = self.start_pos
            else:
                self.pos -= 20
            self.place(x = self.pos, rely= 0, relheight = 1,anchor = 'nw')
            self.front_button.place(x = 10,y= 10, anchor = 'nw')
            self.after(10, self.animate_backwards)    
        else:
            self.in_start_pos = True
            self.is_animating = False  
            self.front_button.place_forget()
    
    def PlaceButton(self):
        self.SideButton.place(x = 10,y=10, anchor = 'nw')

app = App()