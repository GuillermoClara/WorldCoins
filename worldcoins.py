from bs4 import BeautifulSoup
from tkinter import *
from tkinter import ttk
import requests
import threading
import time
from datetime import datetime

# This application implements a currency converter
# using Tkinter GUI library and web scraping technique
# on the site www.x-rates.com


# Class structure
class Currency:
    def __init__(self, name, value_in_usd, symbol):
        self.name = name
        self.value = value_in_usd
        self.symbol = symbol


########################################
# WEB SCRAPING FUNCTIONS               #
########################################

# This function is in charge of loading all currency data from the website and
# convert them into currency objects that can be later be stored in a
# dictionary
def load_currency_list():
    html_text = requests.get(url, header).text

    soup = BeautifulSoup(html_text, 'html.parser')

    usd_coin = Currency('US Dollar', 1.0, 'USD')
    coin_dict = {'US Dollar': usd_coin}

    rates_table = soup.find('table', class_='tablesorter ratesTable')
    currencies = rates_table.find('tbody').findAll('tr')

    for currency in currencies:

        name = currency.find('td').text.strip()
        value = currency.find('td', class_='rtRates').a.text.strip()
        value = float(value)
        ref = (currency.find('td', class_='rtRates').a['href'])
        coin = Currency(name, value, ref[-3:])
        coin_dict[name] = coin

    return coin_dict


# This function updates the values of every
# currency in the dictionary
# Also updates the time last updated
def update_currency_values():
    html_text = requests.get(url, header).text

    soup = BeautifulSoup(html_text, 'html.parser')

    rates_table = soup.find('table', class_='tablesorter ratesTable')
    currencies = rates_table.find('tbody').findAll('tr')

    for currency_element in currencies:
        name = currency_element.find('td').text.strip()
        currency = coin_dictionary.get(name)

        if currency is None:
            continue

        value = currency_element.find('td', class_='rtRates').a.text.strip()
        value = float(value)

        currency.value = value

    calculate()
    current_time = datetime.now()
    time_string = current_time.strftime('%H:%M:%S')
    last_updated.set('Last updated: '+str(time_string))


###########################################
# CURRENCY RELATED FUNCTIONS              #
###########################################

# Function in charge of updating the values from the website
# each 30s
def update_scheduler():
    try:
        update_currency_values()
        time.sleep(30)
        update_scheduler()
    except RuntimeError:
        return


# Function to calculate currencies values according to
# user input
def calculate():
    try:
        amount = float(from_value.get())
        ratio = get_coins_ratio()
        value = abs(amount*ratio)
        to_value.set("{0:.2f}".format(value))

    except ValueError:
        pass


# Gets the ratio between both currencies value in USD
# The ratio serves later to calculate a currency value
# according to user input
def get_coins_ratio():
    from_currency = coin_dictionary.get(initial_from.get())
    to_currency = coin_dictionary.get(initial_to.get())
    return to_currency.value/from_currency.value


# Returns a list of all currencies name from dictionary
def get_currency_list():

    currencies = []
    for coin in coin_dictionary.values():
        currencies.append(coin.name)

    return currencies

###########################################
# GUI RELATED FUNCTIONS                   #
###########################################


# In charge of switching widgets values
def switch():
    calculate()

    # Switching selection values
    temp = initial_from.get()
    initial_from.set(initial_to.get())
    initial_to.set(temp)

    # Switching entry values
    temp = from_value.get()
    from_value.set(to_value.get())
    to_value.set(temp)

    # Switching symbol values
    temp = fr_symbol.get()
    fr_symbol.set(to_symbol.get())
    to_symbol.set(temp)


# Event Handler when user changes
# currency selection
def currency_changed(event, option):
    if option == 'from':
        currency = coin_dictionary.get(initial_from.get())
        fr_symbol.set(currency.symbol)
    elif option == 'to':
        currency = coin_dictionary.get(initial_to.get())
        to_symbol.set(currency.symbol)

    calculate()


# Function in charge of building the application's GUI
def main_gui():

    # Organizing window structure
    for i in range(5):
        root.columnconfigure(index=i, weight=1)
        root.rowconfigure(index=i, weight=1)

    # FROM and TO aesthetic labels

    from_label = Label(root, text='From', font=('Consolas', 20), bg=bg_color, fg=fg_color)
    from_label.grid(row=0, column=1, sticky='s')

    to_label = Label(root, text='To', font=('Consolas', 20), bg=bg_color, fg=fg_color)
    to_label.grid(row=0, column=3, sticky='s')

    # FROM and TO comboBoxes (selections)
    initial_from.set('US Dollar')
    initial_to.set('US Dollar')
    from_options = ttk.Combobox(root, textvariable=initial_from, state='readonly', justify=CENTER,
                                font=('Consolas', 10), height=10, )
    from_options['values'] = get_currency_list()
    from_options.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

    to_options = ttk.Combobox(root, textvariable=initial_to, state='readonly', justify=CENTER, height=10)
    to_options['values'] = get_currency_list()
    to_options.grid(row=1, column=3, sticky='nsew', padx=10, pady=10)

    # FROM and TO entries (for user input)
    from_entry = Entry(root, textvariable=from_value, font=('Consolas', 15), justify=CENTER, bg='#4f4e4d', fg='white')
    from_entry.grid(row=2, column=1, sticky='nsew')

    to_entry = Entry(root, textvariable=to_value, font=('Consolas', 15), justify=CENTER, bg='#4f4e4d', fg='white')
    to_entry.grid(row=2, column=3, sticky='nsew')

    # Symbol labels for both currencies
    from_symbol_label = Label(root, textvariable=fr_symbol, font=('Consolas', 20), bg=bg_color, fg=fg_color)
    from_symbol_label.grid(row=2, column=0, sticky='e')

    to_symbol_label = Label(root, textvariable=to_symbol, font=('Consolas', 20), bg=bg_color, fg=fg_color)
    to_symbol_label.grid(row=2, column=4, sticky='w')

    # Buttons in charge of executing actions
    calc_button = Button(root, text='Calculate', command=calculate, font=('Consolas', 20), bg=fg_color,
                         fg='white', width=10, height=1, activebackground=fg_color,
                         activeforeground='white', relief=FLAT)
    calc_button.grid(row=3, column=2, sticky='nsew', padx=10, pady=10)

    switch_button = Button(root, text='Swap', command=switch, font=('Consolas', 20),
                           bg=fg_color, fg='white', width=10, height=1, activebackground=fg_color,
                           activeforeground='white', relief=FLAT)
    switch_button.grid(row=1, column=2, sticky='nsew', padx=10, pady=10)

    # Event binding to change in comboBox selection
    from_options.bind('<<ComboboxSelected>>', lambda event, opt='from': currency_changed(event, opt))
    to_options.bind('<<ComboboxSelected>>', lambda event, opt='to': currency_changed(event, opt))

    # Label to display most recent currency value update
    updated_info_label = Label(root, textvariable=last_updated, font=('Consolas', 10), bg=bg_color, fg=fg_color)
    updated_info_label.grid(row=4, column=2, sticky='nsew')

    # Update the currencies each 30s in another thread (Multiple processing)
    threading.Thread(target=update_scheduler).start()


################################
# MAIN APPLICATION CODE        #
################################

# Load currencies
coin_dictionary = load_currency_list()


# URL and header are used for web scraping
url = 'https://www.x-rates.com/table/?from=USD&amount=1'
header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/"
                      "99.0.4844.51 Safari/537.36",
        "X-Amzn-Trace-Id": "Root=1-6228d3e0-1613b48566e186fd4764b5f9"}


root = Tk()

# Aesthetic settings
root.title('WorldCoins')
bg_color = '#454442'
fg_color = '#b5c995'
root.config(bg=bg_color)


# Values related to widgets are declared and assigned
# a default value, which is the US dollar
initial_to = StringVar()
initial_from = StringVar()
to_value = StringVar()
to_value.set(1)
from_value = StringVar()
from_value.set(1)

fr_symbol = StringVar()
fr_symbol.set('USD')

to_symbol = StringVar()
to_symbol.set('USD')
last_updated = StringVar()
last_updated.set('Last updated: '+str(datetime.utcnow()))

# Open main window
main_gui()

root.mainloop()
