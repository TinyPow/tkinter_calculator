import customtkinter as ctk
from ctypes import windll
from CalculatorLogic import CalculatorLogic

class CalculatorFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.size = 0
        self.result_variable = ctk.StringVar(value = '0')  # REFERENCED IN LOGIC 
        self.upper_varaible = ctk.StringVar()              # REFERENCED IN LOGIC 

        self.logic = CalculatorLogic(self)

        self.main_frame = MainFrame(self,parent, self.logic, self.result_variable, self.upper_varaible)
        self.main_frame.pack(expand = True, fill = 'both')

        self.side_frame = SideFrame(self,self.logic)

        self.bind('<Configure>', self.Check_size)
                
        self.pack(expand = True, fill = 'both')

    def Check_size(self, event):
        if event.width > 560:
            if self.size == 0:
                self.Expanded_config()
        else:
            if self.size == 1:
                self.Base_config()
    
    def Base_config(self):
        self.main_frame.pack_forget()
        self.side_frame.pack_forget()
        self.main_frame.pack(expand = True, fill = 'both')
        self.size = 0

    def Expanded_config(self):
        self.main_frame.pack_forget()
        self.main_frame.pack(side = 'left',expand = True, fill = 'both')
        self.side_frame.pack(side = 'left', fill = 'both')
        self.size = 1

class SideFrame(ctk.CTkTabview):
    def __init__(self,parent,logic):
        super().__init__(
            parent, 
            width = 280, 
            segmented_button_selected_hover_color='#313131', 
            segmented_button_unselected_hover_color='#313131',
            segmented_button_selected_color='#313131',
            anchor = 'w')
        
        self.button_list = []
        self.logic = logic
        self.tab_history = self.add('History')
        self.tab_memory = self.add('Memory')
        self.first = True
        self.base_label = ctk.CTkLabel(self.tab_history, text = 'No history yet', font = ('Arial',25))
        self.base_label.pack(pady = 20)

    def DeleteHistory(self):
        for button in self.button_list:
            button.pack_forget()
            button.destroy()
        self.first = True
        self.base_label = ctk.CTkLabel(self.tab_history, text = 'No history yet', font = ('Arial',25))
        self.base_label.pack(pady = 20)

    def AddHistory(self, result, top):
        if self.first:
            self.base_label.pack_forget()
            self.first = False
            self.delete_button = ctk.CTkButton(
                self,
                text = 'X',
                font = ('Arial', 20),
                fg_color= '#424242',
                hover_color= '#313131',
                corner_radius= 15,
                width = 50,
                height= 50, 
                command = self.DeleteHistory)
        
        self.delete_button.place( relx= 0.98, rely = 0.99, anchor = 'se')

        self.button_list.append(HistoryButton(self.tab_history,result,top,self.logic))
        self.button_list[len(self.button_list) - 1].pack(fill = 'x')

class HistoryButton(ctk.CTkButton):
    def __init__(self,parent,result,top,logic):
        super().__init__(
            parent,
            text = f'{top}\n{result}',
            text_color = '#878787', 
            font = ('Arial', 30),
            fg_color = 'transparent',
            hover_color= '#313131',
            anchor = 'e',
            command= lambda: logic.History(top,result),
            height = 90,
            width = 260)
        
        self.configure(text = f'{self.WrapLines(top, 260)}\n{result}')
    
    def WrapLines(self, top, width):
        lines = []
        line = ''
        top_divided = []
        temp = ''
        for char in top:
            temp += char
            if char == '(' or char == '+' or char == '-' or char == '/' or char == 'x':
                top_divided.append(temp)
                temp = ''
        top_divided.append(temp)

        for word in top_divided:
            if ctk.CTkFont(family= 'Arial', size = 30).measure(line + word) <= width:
                line += word 
            else:
                lines.append(line)
                line = word
        lines.append(line)
        return '\n'.join(lines)


class MainFrame(ctk.CTkFrame):
    def __init__(self,parent,window,logic, result_variable, upper_variable):
        super().__init__(parent)

        self.top_frame = DisplayFrame(self,window, result_variable,upper_variable)
        self.buttons_frame = ButtonsFrame(self,logic)

        self.buttons_frame.place(relx = 0,rely= 0.3, relwidth = 1,relheight = 0.7)
        self.top_frame.place(relx = 0,rely= 0, relwidth = 1,relheight = 0.3)

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
            # NO IDEA OF HOW IT WORKS
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
