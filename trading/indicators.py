import numpy as np

def moving_average(stock_price, n=7, weights=[]):
    '''
    Calculates the n-day (possibly weighted) moving average for a given stock over time.

    Input:
        stock_price (ndarray): single column with the share prices over time for one stock,
            up to the current day.
        n (int, default 7): period of the moving average (in days).
        weights (list, default []): must be of length n if specified. Indicates the weights
            to use for the weighted average. If empty, return a non-weighted average.
    Output:
        ma (ndarray): the n-day (possibly weighted) moving average of the share price over time.
    Note:
        If n is greater than the stock_price size, then the function will fail.
    '''


    ma = np.zeros(len(stock_price))
    #from day 0 to n, there are no previous days, so the moving average is marked as NaN
    for i in range(n):
        ma[i] = np.nan
    for i in range(n,len(stock_price)):
        #getting the section of the stock price based on the period n
        ma_ls = stock_price[i-n:i]
        #calculating the weighted average, if applicable
        if len(weights) > 0:
            ma_w = []
            for j in range(0,n):
                ma_w.append(ma_ls[j] * weights[j])
            ma[i] = np.average(ma_w)
        else:
            ma[i] = np.average(ma_ls)
    return ma


def oscillator(stock_price, n=7, osc_type='stochastic'):
    '''
    Calculates the level of the stochastic or RSI oscillator with a period of n days.

    Input:
        stock_price (ndarray): single column with the share prices over time for one stock,
            up to the current day.
        n (int, default 7): period of the moving average (in days).
        osc_type (str, default 'stochastic'): either 'stochastic' or 'RSI' to choose an oscillator.

    Output:
        osc (ndarray): the oscillator level with period $n$ for the stock over time.
    '''
    osc = np.zeros(len(stock_price))
    for i in range(n):
        osc[i] = np.nan

    if osc_type == 'stochastic':
        for i in range(n-1,len(stock_price)):
            #getting the section of the stock price based on the period n
            #i-n-1 and i-1 to represent the past 7 days, not including today.
            sto_osc = stock_price[i+1-n:i+1]
            highest = max(sto_osc)
            lowest = min(sto_osc)
            delta = stock_price[i] - lowest
            delta_max = highest - lowest
            osc[i] = delta / delta_max
        return osc

    if osc_type == 'RSI':

        for i in range(n-1, len(stock_price)):
            negative = []
            positive = []
            #getting the section of the stock price based on the period n
            #i-n-1 and i-1 to represent the past 7 days, including today.
            rsi_osc = stock_price[i+1-n:i+1]
            #calucating the difference between consecutive days
            diff = [rsi_osc[j+1] - rsi_osc[j] for j in range(len(rsi_osc)-1)]
            #assigning the differences to positve or negative lists
            for k in range(len(diff)):
                if diff[k] < 0:
                    negative.append(diff[k])
                else:
                    positive.append(diff[k])
            #different RS forumlas, dependent on whether there are any negative or postive values
            #Checks to see if there are any postive or negative values
            if len(negative) == 0:
                pos_avg = np.average(positive)
                rs = pos_avg
            elif len(positive) == 0:
                neg_avg = abs(np.average(negative))
                rs = neg_avg
            else:
                pos_avg = np.average(positive)
                neg_avg = abs(np.average(negative))
                rs = pos_avg / neg_avg
            #RS formula
            osc[i] = 1 - (1 / (1 + rs))
        return osc
