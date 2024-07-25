import customtkinter as ctk
from LogicFile import ConverterLogic

class ConverterFrame(ctk.CTkFrame):
    def __init__(self,parent):
        super().__init__(parent)

        self.top_variable = ctk.StringVar(value='0')
        self.bottom_variable = ctk.StringVar(value = '0')
        self.top_selected = ctk.StringVar()
        self.bottom_selected = ctk.StringVar()

        self.logic = ConverterLogic(self)
        
        self.top_frame = DisplayFrame(self,parent,self.top_variable,self.bottom_variable,self.top_selected,self.bottom_selected, self.logic.currency_names)
        self.buttons_frame = ButtonsFrame(self, self.logic)

        self.buttons_frame.place(relx = 0,rely= 0.45, relwidth = 1,relheight = 0.55)
        self.top_frame.place(relx = 0,rely= 0, relwidth = 1,relheight = 0.45)

        self.pack(expand = True, fill = 'both')

class DisplayFrame(ctk.CTkFrame):
    def __init__(self,parent,window,top_variable,bottom_variable,top_selected,bottom_selected,currency_list):
        super().__init__(parent, fg_color='#2E2E2E')

        self.window = window
        self.top_frame = TopFrame(self)

        self.top = ctk.CTkLabel(self, textvariable=top_variable,font=('Arial', 40), anchor='w')
        self.combo_top = ctk.CTkComboBox(self, values=currency_list , width = 200,variable= top_selected, state = 'readonly')

        self.bottom = ctk.CTkLabel(self,textvariable=bottom_variable, font=('Arial', 40), anchor='w')
        self.combo_bottom = ctk.CTkComboBox(self, values=currency_list, width = 200, variable= bottom_selected, state = 'readonly')
        self.top_frame = TopFrame(self)

        self.combo_top._canvas.bind('<Button-1>',lambda event: self.after(2,parent.logic.Update))
        self.combo_bottom._canvas.bind('<Button-1>',lambda event:self.after(2,parent.logic.Update))

        self.top_frame.place(relx = 1, rely= 0, relwidth = 1, relheight = 0.125, anchor = 'ne')

        self.top.place(x = 20,rely= 0.125,relwidth = 1,relheight = 0.3,anchor = 'nw')  
        self.combo_top.place(x = 20, rely = 0.4, relheight = 0.1, anchor = 'nw')
        self.bottom.place(x = 20,rely= 0.525,relwidth = 1, relheight = 0.3,anchor = 'nw')
        self.combo_bottom.place(x = 20, rely = 0.8, relheight = 0.1, anchor = 'nw')   

class TopFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color= 'transparent')

        self.SideButton = ctk.CTkButton(
            self,
            text_color = 'white', 
            command = parent.window.SideScroll, 
            fg_color='transparent', 
            text= "///", 
            hover_color= '#424242', 
            width= 40,
            font= ('Arial', 22))
        
        self.CurrencyLabel = ctk.CTkLabel(
            self, 
            text_color = 'white', 
            text = 'Currency', 
            font= ('Arial', 22), 
            width=100)

        self.SideButton.place(x = 10,y= 10, anchor = 'nw')
        self.CurrencyLabel.place(x = 50,y= 12, anchor = 'nw')     
        
class ButtonsFrame(ctk.CTkFrame):
    def __init__(self, parent,logic):
        super().__init__(parent)

        self.create_widgets(logic)
        self.create_layout()

    def create_widgets(self,logic):
        Button(self,logic,'0',1,4,'white','#636363')
        # BUTTONS 1-9
        z = 1
        for i in range(3,0,-1):
            for e in range(0,3):
                Button(self,logic,f'{z}',e,i,'white','#636363')
                z += 1
        
        Button(self,logic, ',',2,4,'white','#636363')
        Button(self,logic, 'DEL',2,0,'white','#424242')
        Button(self,logic, 'CE',1,0,'white','#424242')

    def create_layout(self):
        # GRID LAYOUT
        self.rowconfigure((0,1,2,3,4), weight= 1, uniform='a')
        self.columnconfigure((0,1,2), weight=1, uniform='a')

class Button(ctk.CTkButton):
    def __init__(self,parent,logic, text, column, row, text_color, button_color):
        super().__init__(
            parent,
            text= text,
            font=('arial',20),
            hover_color = self.darken_color(button_color, 0.25),
            fg_color= button_color,
            text_color= text_color,
            command= lambda: logic.Input(text))
        
        self.grid(column=column, row=row,sticky="news", padx= 1,pady=1)
    
    def darken_color(self,color, factor):
        factor = 1 - factor
        red = int(int(color[1:3],16) * factor)
        green = int(int(color[3:5],16)* factor)
        blue = int(int(color[5:7], 16) * factor)

        return(f'#{hex(red)[2:]}{hex(green)[2:]}{hex(blue)[2:]}')