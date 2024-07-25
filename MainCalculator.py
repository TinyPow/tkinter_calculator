import customtkinter as ctk
from ctypes import windll
from LogicFile import CalculatorLogic

class CalculatorFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.result_variable = ctk.StringVar(value = '0')  # REFERENCED IN LOGIC 
        self.upper_varaible = ctk.StringVar()              # REFERENCED IN LOGIC 

        self.logic = CalculatorLogic(self)

        self.top_frame = DisplayFrame(self,parent, self.result_variable,self.upper_varaible)
        self.buttons_frame = ButtonsFrame(self,self.logic)

        self.buttons_frame.place(relx = 0,rely= 0.3, relwidth = 1,relheight = 0.7)
        self.top_frame.place(relx = 0,rely= 0, relwidth = 1,relheight = 0.3)

        self.pack(expand = True, fill = 'both')

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
        
        self.MinimizeButton = ctk.CTkButton(
            self,
            text_color = 'white', 
            command = parent.ChangeSide, 
            fg_color='transparent', 
            text= parent.ButtonText, 
            hover_color= '#424242', 
            font= ('Arial', 22),
            width=40)
        
        self.StandardLabel = ctk.CTkLabel(
            self, 
            text_color = 'white', 
            text = 'Standard', 
            font= ('Arial', 22), 
            width=100)

        self.SideButton.place(x = 10,y= 10, anchor = 'nw')
        self.StandardLabel.place(x = 50,y= 12, anchor = 'nw')
        self.MinimizeButton.place(x = 150,y= 8, anchor = 'nw')
      
class DisplayFrame(ctk.CTkFrame):
    def __init__(self,parent,window, result_variable, upper_variable):
        super().__init__(parent, fg_color='#2E2E2E')

        self.window = window

        self.ButtonText = '|||'
        self.MaxSize = True
        self.result_variable = result_variable
        self.upper_variable = upper_variable

        self.top_frame = TopFrame(self)

        self.create_widgets()
        self.create_layout()

    def create_widgets(self):

        self.place_reset()

        self.results = ctk.CTkLabel(self, textvariable= self.result_variable,font=('Arial', 60), anchor='e')
        
        if self.MaxSize:
            try:
                self.title_bar.place_forget()
            except:
                pass
            self.previous = ctk.CTkLabel(self,textvariable=self.upper_variable, font=('Arial', 30), text_color= '#878787', anchor='e')
            self.top_frame = TopFrame(self)

        else:
            self.title_bar = TitleBar(self.window,self)

    def place_reset(self):
            try:
                self.previous.place_forget()
                self.top_frame.place_forget()
                self.results.place_forget()
            except:
                pass

    def create_layout(self):
        if self.MaxSize:
            self.previous.place(relx =0.95,rely= 0.35,relwidth = 1,relheight = 0.2,anchor = 'ne')     
            self.top_frame.place(relx = 1, rely= 0, relwidth = 1, relheight = 0.3, anchor = 'ne')
            self.results.place(relx =0.98,rely= 0.55,relwidth = 1, relheight = 0.45,anchor = 'ne')

        else:    
            self.title_bar.place(relx = 0, rely = 0 ,relwidth = 1)
            self.results.place(relx =0.98,rely= 0.3,relwidth = 1, relheight = 0.5,anchor = 'ne')

    def ChangeSide(self):
        if self.MaxSize:
            self.window.attributes('-topmost', True)
            self.window.overrideredirect(True)
            self.window.update_idletasks()
            self.window.withdraw()
            self.set_appwindow()
            self.MaxSize = False
            self.ButtonText = '|||'
            self.window.geometry('300x500')
            self.create_widgets()
            self.create_layout()
        else:
            self.window.attributes('-topmost', False)
            self.window.overrideredirect(False)
            self.MaxSize = True
            self.ButtonText = '|||'
            self.window.geometry('500x700')
            self.create_widgets()
            self.create_layout()
    
    def set_appwindow(self):
            # NO IDEA DI COME FUNZIONA MA FUNZIONA
            GWL_EXSTYLE=-20
            WS_EX_APPWINDOW=0x00040000
            WS_EX_TOOLWINDOW=0x00000080
            hwnd = windll.user32.GetParent(self.window.winfo_id())
            style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            style = style & ~WS_EX_TOOLWINDOW
            style = style | WS_EX_APPWINDOW
            res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
            self.window.withdraw()
            self.window.after(10, lambda:self.window.wm_deiconify())

class TitleBar(ctk.CTkFrame):
    def __init__(self,window,frame):
        super().__init__(window, height = 40, fg_color='#2E2E2E')
        self.window = window

        self.ExitButton = ctk.CTkButton(self, text = 'X', fg_color= 'transparent', hover_color= 'red', command = window.destroy,corner_radius= 0 )
        self.ExitButton.place(relx = 1, rely = 0, anchor = 'ne' , relwidth = 0.2, relheight = 1)

        self.MinimizeButton = ctk.CTkButton(self,text_color = 'white', command = frame.ChangeSide, fg_color='transparent', text= frame.ButtonText, hover_color= '#424242')
        self.MinimizeButton.place(relx = 0, rely = 0, relwidth = 0.22, relheight = 1, anchor = 'nw')

        self._offsetx = 0
        self._offsety = 0
        self.bind("<Button-1>" ,self.clickwin)
        self.bind("<B1-Motion>", self.dragwin)
    
    def dragwin(self,event):
        x = self.window.winfo_pointerx() - self._offsetx
        y = self.window.winfo_pointery() - self._offsety
        
        self.window.geometry(f"+{x}+{y}")

    def clickwin(self,event):
        self._offsetx = self.window.winfo_pointerx() - self.window.winfo_rootx()
        self._offsety = self.window.winfo_pointery() - self.window.winfo_rooty()

class ButtonsFrame(ctk.CTkFrame):
    def __init__(self, parent,logic):
        super().__init__(parent)

        self.create_widgets(logic)
        self.create_layout()

    def create_widgets(self,logic):
        Button(self,logic,'0',1,5,'white','#636363')
        # BUTTONS 1-9
        z = 1
        for i in range(4,1,-1):
            for e in range(3):
                Button(self,logic,f'{z}',e,i,'white','#636363')
                z += 1
        
        Button(self,logic, '+/-',0,5,'white','#636363')
        Button(self,logic, ',',2,5,'white','#636363')
        Button(self,logic, '=',3,5,'black','#b3b3b3')
        Button(self,logic, '+',3,4,'white','#424242')
        Button(self,logic, '-',3,3,'white','#424242')
        Button(self,logic, 'x',3,2,'white','#424242')
        Button(self,logic, '/',3,1,'white','#424242')
        Button(self,logic, 'DEL',3,0,'white','#424242')
        Button(self,logic, '%',0,0,'white','#424242')
        Button(self,logic, 'CE',1,0,'white','#424242')
        Button(self,logic, 'C', 2,0,'white','#424242')
        Button(self,logic, '1/x',0,1,'white','#424242')
        Button(self,logic, 'x²',1,1,'white','#424242')
        Button(self,logic, '√x',2,1,'white','#424242')

    def create_layout(self):
        # GRID LAYOUT
        self.rowconfigure((0,1,2,3,4,5), weight= 1, uniform='a')
        self.columnconfigure((0,1,2,3), weight=1, uniform='a')

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
