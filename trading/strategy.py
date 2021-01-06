# Functions to implement our trading strategy.
import numpy as np
from trading import process as proc
from trading import indicators as ind

def random(stock_prices, period=7, amount=5000, fees=20, ledger='ledger_random.txt'):
    '''
    Randomly decides, every period, which stocks to purchase,
    do nothing, or sell (with equal probability).
    Spends a maximum of amount on every purchase.

    Input:
        stock_prices (ndarray): the stock price data
        period (int, default 7): how often we buy/sell (days)
        amount (float, default 5000): how much we spend on each purchase
            (must cover fees)
        fees (float, default 20): transaction fees
        ledger (str): path to the ledger file

    Output: None
    '''

    N = len(stock_prices[0])
    #creates inital portfolio
    portfolio = proc.create_portfolio([amount] * N, stock_prices, fees, ledger)
    #creates array of boolean data to check if the stock prices are NaN or not
    nan_check = np.isnan(stock_prices)
    #loops through each date other a set period
    #period - 1 as it is the 7th day after the portfolio was created
    for date in range(period - 1, len(stock_prices)-1, period):
        #equal probabilty of buy sell or nothing
        choice = np.random.choice(['buy', 'sell', 'nothing'])
        #chooses a random integer, added a +1 to len(stock_prices[0]) to select all potential values
        num_stocks = np.random.randint(0,len(stock_prices[0]) + 1)
        #gets a random array of numbers that represent a the index of the stocks in stock_prices
        stocks = np.random.choice(len(stock_prices[0]), num_stocks, replace=False)
        if choice == 'buy':
            for stock in stocks:
                if nan_check[date][stock] == False:
                    proc.buy(date, stock, amount, stock_prices, fees, portfolio, ledger)
        if choice == 'sell':
            for stock in stocks:
                if nan_check[date][stock] == False and portfolio[stock] > 0:
                    proc.sell(date, stock, stock_prices, fees, portfolio, ledger)
    # Sell all the stocks on the last day
    for stock in range(len(portfolio)):
        if nan_check[len(stock_prices)-1][stock] == False and portfolio[stock] > 0:
            proc.sell(len(stock_prices)-1, stock, stock_prices, fees, portfolio, ledger)
    return None


def crossing_averages(stock_prices, n=50, m=200, amount=5000, weights_n=[], weights_m=[], fees=20, ledger='ledger_crossing_averages.txt'):
    '''
    Calculates a slow moving average (SMA) and a fast moving average (FMA).  Strategy is
    on the FMA crossing the SMA.  If it crosses as the FMA is increasing but the SMA is decreasing
    then it buys, and if the FMA is decreasing but the SMA is increasing then it sells.
    Spends a maximum of amount on every purchase.

    Input:
    stock_prices (ndarray): the stock price data
    n (int, default 50): Slow moving average period (days)
    m (int, default 200): Fast moving average period (days)
    amount (float, default 5000): how much we spend on each purchase
        (must cover fees)
    weights_n (list, default []): must be of length n if specified. Indicates the weights
        to use for the weighted average. If empty, return a non-weighted average.
    weights_m (list, default []): must be of length n if specified. Indicates the weights
        to use for the weighted average. If empty, return a non-weighted average.
    fees (float, default 20): transaction fees
    ledger (str): path to the ledger file

    Output: FMA (ndarray): Fast moving average data
            SMA (ndarray): Slow moving average data
    '''

    N = len(stock_prices[0])
    #creates inital portfolio
    portfolio = proc.create_portfolio([amount] * N, stock_prices, fees, ledger)
    #creates array of boolean values to check if the stock prices are NaN or not
    nan_check = np.isnan(stock_prices)
    #loops through each stock
    for stock in range(N):
        stock_price = stock_prices[:,stock]
        SMA = ind.moving_average(stock_price, n, weights_n)
        FMA = ind.moving_average(stock_price, m, weights_m)
        nan_check_SMA = np.isnan(SMA)
        nan_check_FMA = np.isnan(FMA)
        #loops through each date
        for date in range(len(stock_prices)):
            if nan_check_SMA[date] == True or nan_check_FMA[date] == True:
                pass
            else:
                #Decided if they are equal then they should treat it as if it crossed
                if FMA[date] >= SMA[date] and FMA[date-1] < SMA[date-1]:
                    proc.buy(date, stock, amount, stock_prices, fees, portfolio, ledger)
                if FMA[date] <= SMA[date] and FMA[date-1] > SMA[date-1]:
                    if portfolio[stock] > 0:
                        proc.sell(date, stock, stock_prices, fees, portfolio, ledger)
    #Sell all the stocks on the last day
    for stock in range(len(portfolio)):
        if nan_check[len(stock_prices)-1][stock] == False and portfolio[stock] > 0:
            proc.sell(len(stock_prices)-1, stock, stock_prices, fees, portfolio, ledger)
    return FMA, SMA

def momentum(stock_prices, osc_type='stochastic', n=7, cool_off=7, amount=5000, fees=20, ledger='ledger_momentum.txt'):
    '''
        Uses the oscillators RSI or stochastic to determine when to sell and buy.
        Spends a maximum of amount on every purchase.

        Input:
        stock_prices (ndarray): the stock price data
        osc_type (str, default stochastic): RSI or stochastic
        n (int, default 7): Period (days)
        cool_off (int, default 7): Cool off period for buying or selling
        amount (float, default 5000): how much we spend on each purchase
            (must cover fees)
        fees (float, default 20): transaction fees
        ledger (str): path to the ledger file

        Output:
        osc (ndarray): The oscillator data
    '''

    N = len(stock_prices[0])
    #creates inital portfolio
    portfolio = proc.create_portfolio([amount] * N, stock_prices, fees, ledger)
    #creates array of boolean values to check if the stock prices are NaN or not
    nan_check = np.isnan(stock_prices)
    for stock in range(N):
    #loops through each stock
        stock_price = stock_prices[:,stock]
        if osc_type == 'stochastic':
            osc = ind.oscillator(stock_price, n, 'stochastic')
        elif osc_type == 'RSI':
            osc = ind.oscillator(stock_price, n, 'RSI')
        nan_check_osc = np.isnan(osc)
        #reset the date count
        date = 0
        #use while loop so cool_off time could be added easily
        while date < len(stock_prices):
            if nan_check_osc[date] == False:
                if 0.7 <= osc[date] <= 0.8:
                    if portfolio[stock] > 0:
                        proc.sell(date, stock, stock_prices, fees, portfolio, ledger)
                        date += (cool_off - 1)
                elif 0.2 <= osc[date] <= 0.3:
                    proc.buy(date, stock, amount, stock_prices, fees, portfolio, ledger)
                    date += (cool_off - 1)
            date += 1
    #Sell all the stocks on the last day
    for stock in range(len(portfolio)):
        if nan_check[len(stock_prices)-1][stock] == False and portfolio[stock] > 0:
            proc.sell(len(stock_prices)-1, stock, stock_prices, fees, portfolio, ledger)
    return osc
