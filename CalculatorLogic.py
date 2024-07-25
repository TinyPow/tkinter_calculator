from math import sqrt

class CalculatorLogic:
    def __init__(self,window):
        self.window = window
        self.input_list = [['0'],'',[]]
        self.sign = ['', '']
        self.previous_state = 0

        self.history = [[''],'',[]]
        self.history_sign = ['', '']

        self.modifier1 = []
        self.modifier2 = []
        self.modifierVar1 = False
        self.modifierVar2 = False
        self.modifierFirst1 = ''
        self.modifierFirst2 = ''

        self.state = 0
        self.dot = False
        self.maxLen = 15
        self.upper = self.window.upper_varaible
    
    def TotalLen(self):
        return len(self.input_list[0]) + len(self.input_list[1]) + 2

    def Input(self,text):
        if text == ',':
            text = '.'

        if (text.isdigit() or text == '.') and self.TotalLen() < self.maxLen:
            if (self.state == 0 and self.modifierVar1 == True):
                self.Reset()
            if (self.state == 2 and self.modifierVar2 == True):
                self.Reset2()

            if (self.state == 'END' or self.state == "ERROR" ):
                self.Reset()

            if text == '.' and self.dot == True:
                pass
            else:
                if(self.state == 0):
                    if(self.input_list[0] == ['0'] and text != '.'):
                        self.input_list[0] = []
                    self.input_list[0].append(text)
                else:
                    self.input_list[2].append(text)
                    self.state = 2

            if text == '.':
                self.dot = True

        elif self.IsOperator(text) and (self.state == 0 or self.state == 'END' or self.state == 2):
            if (self.state == 2):
                self.Calculate()

            self.dot = False
            self.input_list[1] = text
            self.state = 1

        elif text == 'DEL':
            self.Delete()
        
        elif text == '=' and self.state == 2:
            self.Calculate()

        
        elif text == '+/-':
            if self.state == 0 or self.state == 'END':
                if self.modifierVar1:
                    self.Modifier(text,0)
                if self.sign[0] == '':
                    self.sign[0] = '-'
                else:
                    self.sign[0] = ''
            elif self.state == 2:
                if self.modifierVar2:
                    self.Modifier(text,2)
                if self.sign[1] == '':
                    self.sign[1] = '-'
                else:
                    self.sign[1] = ''
        
        elif self.IsModifier(text) and (self.state == 0 or self.state == 'END' or self.state == 2):
            if self.state == 0 or self.state == 'END':
                result = self.Modifier(text, 0)
                self.input_list[0] = []
                self.input_list[0].append(result)
            else:
                result = self.Modifier(text, 2)
                self.input_list[2] = []
                self.input_list[2].append(result)
            self.dot = False

        elif text == 'CE':
            if self.state == 2:
                self.Reset2()
            else:
                self.Reset()

        
        elif text == 'C':
            self.Reset()


        self.UpdateTop()
        self.UpdateText()

    def Reset2(self):
        self.previous_state = self.state
        self.modifier2 = []
        self.modifierVar2 = False
        self.modifierFirst2 = ''
        self.state = 1
        self.sign[1] = ''
        self.input_list[2] = []
        self.dot = False

    def Reset(self):
        self.previous_state = 0
        self.history = [[''],'',[]]
        self.history_sign = ['', '']
        self.input_list = [['0'],'',[]]
        self.sign = ['', '']
        self.state = 0
        self.dot = False
        self.modifier1 = []
        self.modifier2 = []
        self.modifierVar1 = False
        self.modifierVar2 = False
        self.modifierFirst1 = ''
        self.modifierFirst2 = '' 

    def IsModifier(self,char):
        if char == '1/x' or char == '√x' or char == 'x²'or char == '%':
            return True
        else:
            return False
        
    def IsOperator(self,char): 
        if char == '+' or char == '-'  or char == 'x' or char == '/':
            return True
        else:
            return False
        
    def Modifier(self, input, index):
        if len(self.modifier1) + len(self.modifier2) > 10:
            self.state == "ERROR"
            return 'ERROR'  

        self.history = self.input_list.copy()
        self.history_sign = self.sign.copy()
        oldterm = self.ParseList(self.input_list[index])
        term = float(oldterm)
        
        if index == 2:
            index = 1

        match input:
            case '+/-':
                pass
            case '1/x':
                if term == 0.0:
                    term = 'ERROR'
                    self.state = 'ERROR'
                else:
                    term = 1/term
            case '√x':
                if self.sign[index] == '':    
                    term = sqrt(term)
                else:
                    term = 'ERROR'
                    self.state = 'ERROR'
            case 'x²':
                term = term ** 2
                self.sign[index] == ''
            case '%':
                term = term/100
        
        if term != 'ERROR':
            if index == 0:
                if (self.modifierVar1 == False):
                    self.modifierFirst1 = f'{self.sign[0]}{oldterm}'
                self.modifierVar1 = True
            if index == 1:
                if (self.modifierVar2 == False):
                    self.modifierFirst2 = f'{self.sign[1]}{oldterm}'
                self.modifierVar2 = True

            self.modifier = True
            term = round(term,5)
            if int(term) == float(term):
                term = int(term)

            if self.state == 0:
                self.modifier1.append(input)
            elif self.state == 2:
                self.modifier2.append(input)
            elif self.state == 'END':
                self.modifier1.append(input)
                self.state = 0
        
            return term
    
    def UpdateTop(self):
        term1 = self.ParseList(self.input_list[0]).replace('.', ',')
        term2 = self.ParseList(self.input_list[2]).replace('.', ',')
        term1.replace(' ', '')
        term2.replace(' ', '')

        history1 = self.ParseList(self.history[0]).replace('.', ',')
        history2 = self.ParseList(self.history[2]).replace('.', ',')

        if (self.state == 0):
            if (self.modifierVar1):
                self.upper.set(self.ModifierParse(self.modifier1,self.modifierFirst1))
            else:
                self.upper.set('')
        elif (self.state == 1):
            if (self.modifierVar1):
                self.upper.set(f'{self.ModifierParse(self.modifier1,self.modifierFirst1)} {self.input_list[1]}')
            else:
                self.upper.set(f'{self.sign[0]}{term1} {self.input_list[1]}') 
        elif (self.state == 2):
            if (self.modifierVar2):
                if(self.modifierVar1):
                    self.upper.set(f'{self.ModifierParse(self.modifier1,self.modifierFirst1)} {self.input_list[1]} {self.ModifierParse(self.modifier2, self.modifierFirst2)}')
                else:
                    self.upper.set(f'{self.sign[0]}{term1} {self.input_list[1]} {self.ModifierParse(self.modifier2, self.modifierFirst2)}')
        elif (self.state == 'END'):
            if (self.modifierVar1 and self.modifierVar2):
                self.upper.set(f'{self.ModifierParse(self.modifier1,self.modifierFirst1)} {self.history[1]} {self.ModifierParse(self.modifier2, self.modifierFirst2)} =')
            elif(self.modifierVar1):
                self.upper.set(f'{self.ModifierParse(self.modifier1,self.modifierFirst1)} {self.history[1]} {self.history_sign[0]}{history2} =')
            elif(self.modifierVar2):
                self.upper.set(f'{self.history_sign[0]}{history1} {self.history[1]} {self.ModifierParse(self.modifier2, self.modifierFirst2)} =')
            else:
                self.upper.set(f'{self.history_sign[0]}{history1} {self.history[1]} {self.history_sign[0]}{history2} =')   
            
            self.modifier1 = []
            self.modifier2 = []
            self.modifierFirst1 = ''
            self.modifierFirst2 = ''
            self.modifierVar1 = False
            self.modifierVar2 = False    

    def UpdateText(self):
        term1 = self.ParseList(self.input_list[0]).replace('.', ',')
        term2 = self.ParseList(self.input_list[2]).replace('.', ',')
        term1.replace(' ', '')
        term2.replace(' ', '')
        if (self.state == 2):
            if term2 == '':
                self.window.result_variable.set('0')
            else:
                self.window.result_variable.set(f'{self.sign[1]}{term2}')
        elif(self.state == "ERROR"):
            self.window.result_variable.set('ERROR')
            self.upper.set('')
        elif self.previous_state == 2:
            self.window.result_variable.set('0')
        else:
            self.window.result_variable.set(f'{self.sign[0]}{term1}')

    def ModifierParse(self,old_list,number):
        result = ''
        input_list = old_list.copy()
        input_list.reverse()
        for element in input_list:
            match element:
                case '+/-':
                    result += 'negate('
                case '1/x':
                    result += '1/('
                case '√x':
                    result += '√('
                case 'x²':
                    result += 'sqr('
                case '%':
                    result += '1/100('  
        result += number
        for i in range(len(input_list)):
            result += ')'
        return result.replace('.', ',')

    def ParseList(self,list):
        result = ''
        for element in list:
            result += f'{element}'
        return result
    
    def Delete(self):
        match self.state:
            case 0:
                if(self.modifierVar1):
                    self.Reset()
                else:
                    if (self.input_list[0]) != []:
                        self.input_list[0] .pop()
                    if(self.input_list[0] == []):
                        self.Reset()
            case 1:
                self.input_list[1] = ''
                self.state = 0
            case 2:
                if(self.modifierVar2):
                    self.Reset2()
                else:
                    if (self.input_list[2]) != []:
                        self.input_list[2].pop()
            case 'END':
                self.Reset()
            case 'ERROR':
                self.Reset()

    def Calculate(self):
        self.history = self.input_list.copy()
        self.history_sign = self.sign.copy()
        term1 = float(self.ParseList(self.input_list[0]))
        term2 = float(self.ParseList(self.input_list[2])) 

        if self.sign[0] == '-':
            term1 *= -1
        if self.sign[1] == '-':
            term2 *= -1

        match self.input_list[1]:
            case '+':
                result = term1 + term2
            case '-':
                result = term1 - term2
            case 'x':
                result = term1 * term2
            case '/':
                if term2 == 0:
                    result = "ERROR"
                    self.state = 'ERROR'
                else:
                    result = float(term1 / term2)
        
        if result != "ERROR":
            result = round(result,5)
            if result < 0:
                self.sign[0] = '-'
                result = abs(result)
            
            if int(result) == float(result):
                result = int(result)
            
            self.state = 'END'

        self.dot = False
        self.previous_state = 0
        self.sign[1] = ''
        self.input_list = [[],'',[]]
        self.input_list[0].append(f'{result}')
