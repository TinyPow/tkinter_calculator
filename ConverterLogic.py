import requests
import yaml
import os.path
import json

class ConverterLogic:
    def __init__(self, frame):
        self.frame = frame
        self.currency = dict()

        if(os.path.isfile('currency_values.json')):
            with open('currency_values.json') as currency_values_json:
                data = json.load(currency_values_json)
                values_raw = data['response']['rates']
        else:
            try:
                with open('api_key.yaml') as api_key_file:
                    api_key_yaml = yaml.safe_load(api_key_file)
                    api_key = api_key_yaml['api_key']
            except FileNotFoundError:
                print('NO api_key.yaml FILE FOUND')
            except KeyError:
                print('NO api_key VALUE IN YAML FILE')
            api_url = f"https://api.currencybeacon.com/v1/latest?api_key={api_key}&base=USD"
            response = requests.get(api_url)
            currency_values = response.json()
            values_raw = currency_values['response']['rates']
            with open('currency_values.json', 'w') as currency_values_json:
                json.dump(currency_values,currency_values_json)

        self.currency_symble = {
            'USA - Dollar' : 'USD', 
            'Europe - Euro' : 'EUR', 
            'Japan - Yen' : 'JPY', 
            'UK - Pound' : 'GBP', 
            'China - Renminbi' : 'CNY', 
            'Australia - Dollar' : 'AUD',
            'Canada - Dollar' : 'CAD',
            'Switzerland - Franc' : 'CHF',
            'Hong Kong - Dollar' : 'HKD',
            'Singapore - Dollar' : 'SGD',
            'Sweden - Corona' : 'SEK',
            'South Korea - Won' : 'KRW',
            'Norway - Krone' : 'NOK',
            'New Zealand - Dollar' : 'NZD',
            'India - Rupee' : 'INR',
            'Mexico - Peso' : 'MXN',
            'Taiwan - Dollar' : 'TWD',
            'South Africa - Rand' : 'ZAR',
            'Brazil - Real' : 'BRL' }
        
        for key,element in self.currency_symble.items():
            self.currency.update({key:values_raw[element]})

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