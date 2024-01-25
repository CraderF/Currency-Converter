import requests
import wx
import os

from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('API_KeyExchange')


class MyPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

class ConverterFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='Currency Converter')

        self.panel = MyPanel(self)
        self.currency_converter = CurrencyConverter()

        self.from_currencyLabel = wx.StaticText(self.panel, label="From Currency")
        self.from_currencyChoice = wx.Choice(self.panel, choices=self.currency_converter.get_exchange_rates())

        self.to_currencyLabel = wx.StaticText(self.panel, label="To Currency")
        self.to_currencyChoice = wx.Choice(self.panel, choices=self.currency_converter.get_exchange_rates())

        self.amountLabel = wx.StaticText(self.panel, label="Amount:")
        self.amountInput = wx.TextCtrl(self.panel)

        self.resultLabel = wx.StaticText(self.panel, label="Result:")
        self.resultDisp = wx.TextCtrl(self.panel, style=wx.TE_READONLY)
        

        sizer = wx.GridBagSizer(10, 10)
        sizer.Add(self.from_currencyLabel, (0, 0))
        sizer.Add(self.from_currencyChoice, (0, 1))
        sizer.Add(self.to_currencyLabel, (1, 0))
        sizer.Add(self.to_currencyChoice, (1, 1))
        sizer.Add(self.amountLabel, (2, 0))
        sizer.Add(self.amountInput, (2, 1))
        sizer.Add(self.resultLabel, (3, 0))
        sizer.Add(self.resultDisp, (3, 1))

        self.panel.SetSizerAndFit(sizer)
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        self.Destroy()


class CurrencyConverter:
    def __init__(self):
        self.conversion_rates = self.get_exchange_rates()
            
    def get_exchange_rates(self):
        response = requests.get(api_key)
        data = response.json()
        return list(data["conversion_rates"])

    def get_valid_currency_input(self, message):
        while True:
            currency = input(message)
            if currency in self.conversion_rates:
                print(f"Selected Currency: {currency}")
                return currency
            else:
                print("Please enter a valid currency.")

    def convert_currency(self, from_currency, to_currency, amount):
        conversion_rate = self.conversion_rates[to_currency]
        converted_amount = amount * conversion_rate
        return converted_amount

    def run_conversion(self):
        from_currency = self.get_valid_currency_input("Enter the currency you want to convert from: ")
        to_currency = self.get_valid_currency_input("Enter the currency you want to convert to: ")
        from_amount = float(input(f"Enter the amount of {from_currency}: "))

        to_amount = self.convert_currency(from_currency, to_currency, from_amount)

        print(f"{from_amount} {from_currency} is equivalent to {to_amount} {to_currency}")

if __name__ == '__main__':
    app = wx.App(redirect=False)
    frame = ConverterFrame()
    frame.Show()
    app.MainLoop()






