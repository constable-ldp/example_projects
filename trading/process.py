# Functions to process transactions.
import numpy as np
import os

def log_transaction(transaction_type, date, stock, number_of_shares, price, fees, ledger_file):
    '''
    Records a transaction in the file, ledger_file.

    Input:
        transaction_type (str): 'buy' or 'sell'
        date (int): the date of the transaction (nb of days since day 0)
        stock (int): the stock we buy or sell (the column index in the data array)
        number_of_shares (int): the number of shares bought or sold
        price (float): the price of a share at the time of the transaction
        fees (float): transaction fees (fixed amount per transaction, independent of the number of shares)
        ledger_file (str): path to the ledger file

    Output: None.
        Writes one line in the ledger file to record a transaction with the input information.

    '''
    #creates file if empty and appends string to file
    f = open(ledger_file, 'a+')
    string = str(transaction_type) + ',' + str(date) + ',' + str(stock) + ',' + str(number_of_shares)\
            + ',' + format(price, '.2f') + ',' + str(round(fees,2)) + ',' +\
            str(format((-number_of_shares * price) - fees, '.2f'))
    f.write(string)
    f.write('\n')
    f.close()
    return None

def buy(date, stock, available_capital, stock_prices, fees, portfolio, ledger_file):
    '''
    Buy shares of a given stock, with a certain amount of money available.
    Updates portfolio in-place, logs transaction in ledger.

    Input:
        date (int): the date of the transaction (nb of days since day 0)
        stock (int): the stock we want to buy
        available_capital (float): the total (maximum) amount to spend,
            this must also cover fees
        stock_prices (ndarray): the stock price data
        fees (float): total transaction fees (fixed amount per transaction)
        portfolio (list): our current portfolio
        ledger_file (str): path to the ledger file

    Output: None
    '''
    price = stock_prices[date][stock]
    number_of_shares = int((available_capital - fees) / price)
    if number_of_shares > 0:
        log_transaction('buy', date, stock, number_of_shares, price, fees, ledger_file)
        portfolio[stock] += number_of_shares
    else:
        print('You do not have enough capital to buy these shares.')

def sell(date, stock, stock_prices, fees, portfolio, ledger_file):
    '''
    Sell all shares of a given stock.
    Updates portfolio in-place, logs transaction in ledger.

    Input:
        date (int): the date of the transaction (nb of days since day 0)
        stock (int): the stock we want to sell
        stock_prices (ndarray): the stock price data
        fees (float): transaction fees (fixed amount per transaction)
        portfolio (list): our current portfolio
        ledger_file (str): path to the ledger file

    Output: None
    '''
    price = stock_prices[date][stock]
    number_of_shares = portfolio[stock]
    portfolio[stock] = 0
    log_transaction('sell', date, stock, number_of_shares, -price, fees, ledger_file)

def create_portfolio(available_amounts, stock_prices, fees, ledger_file):
    '''
    Creates a portfolio by buying a given number of shares of each stock.

    Input:
        available_amounts (list): how much money we allocate to the initial
            purchase for each stock (this should cover fees)
        stock_prices (ndarray): the stock price data
        fees (float): transaction fees (fixed amount per transaction)

    Output:
        portfolio (list): the initial portfolio
    '''
    #removes old file so new data doesn't get added to old file
    if os.path.exists(ledger_file):
        os.remove(ledger_file)
    portfolio = [0] * len(stock_prices[0])
    for i in range(len(stock_prices[0])):
        buy(0, i, available_amounts[i], stock_prices, fees, portfolio, ledger_file)
    return portfolio
