class ConverterLogic:
    def __init__(self, frame):
        self.frame = frame
        self.currency = {
            'USA - Dollar' : 1, 
            'Europe - Euro' : 0.92, 
            'Japan - Yen' : 157.54, 
            'UK - Pound' : 0.77, 
            'China - Renminbi' : 7.26, 
            'Australia - Dollar' : 1.49,
            'Canada - Dollar' : 1.37,
            'Switzerland - Franc' : 0.88,
            'Hong Kong - Dollar' : 7.81,
            'Singapore - Dollar' : 1.34,
            'Sweden - Corona' : 10.68,
            'South Korea - Won' : 1.39,
            'Norway - Krone' : 10.92,
            'New Zealand - Dollar' : 1.66,
            'India - Rupee' : 83.72,
            'Mexico - Peso' : 18.05,
            'Taiwan - Dollar' : 32.82,
            'South Africa - Rand' : 18.28,
            'Brazil - Real' : 5.60 }

        self.currency_names = []

        for element in self.currency:
            self.currency_names.append(element)
        
        self.top_variable = frame.top_variable
        self.bottom_variable = frame.bottom_variable
        self.top_selected = frame.top_selected
        self.bottom_selected = frame.bottom_selected

        self.top_selected.set('USA - Dollar')
        self.bottom_selected.set('Europe - Euro')

        self.input_list = []
        self.comma = False

    def Input(self,text):
        if text.isdigit() and len(self.input_list) < 10:
            if text == '0' and text[0] == '0':
                pass
            else:
                self.input_list.append(text)
            
        if text == ',' and self.comma == False:
            self.comma = True
            self.input_list.append('.')
        
        if text == 'DEL':
            if self.input_list != []:
                removed = self.input_list.pop()
                if removed == '.':
                    self.comma = False

        if text == 'CE':
            self.comma = False
            self.input_list = []

        self.Update()

    def Update(self):
        self.risultato = self.Calculate()
        self.Display()

    def Calculate(self):
        parsed_list = self.ParseList(self.input_list)
        if parsed_list == '':
            parsed_list = '0'
        valore_iniziale = float(parsed_list)
        valuta_top = self.currency[self.top_selected.get()]
        valuta_bot = self.currency[self.bottom_selected.get()]

        risultato = (valore_iniziale/valuta_top)*valuta_bot

        risultato = round(risultato,2)

        if int(risultato) == float(risultato):
                risultato = int(risultato)

        return f'{risultato}'

    def Display(self):
        # TOP TERM
        term1 = self.ParseList(self.input_list).replace('.', ',')
        if term1 == '':
            self.top_variable.set('0')
        elif term1[0] == ',':
            self.top_variable.set(f'0{term1}')
        else:
            self.top_variable.set(term1)

        # BOTTOM TERM
        self.bottom_variable.set(self.risultato)

    def ParseList(self,list):
        result = ''
        for element in list:
            result += f'{element}'
        return result