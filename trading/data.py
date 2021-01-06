import numpy as np

def generate_stock_price(days, initial_price, volatility):
    '''
    Generates share prices for a given number of companies,
    with a given inital price and volatility after a given
    number of days.

    Input:
        days (ndarray): the stock price data
        period (int, default 7): how often we buy/sell (days)
        amount (float, default 5000): how much we spend on each purchase
            (must cover fees)
        fees (float, default 20): transaction fees

    Output: stock_prices (ndarray): the generated stock price data
    '''

    #number of companies
    n = len(initial_price)
    #creating an array to store the stock_prices
    stock_prices = np.zeros([days,n])
    #first row is initial price
    stock_prices[0] = initial_price
    #using numpy to set up a random generator
    rng = np.random.default_rng()
    #drift array to store total drift, allows for max duration (14 days) to avoid errors
    drift = np.zeros([days + 14,n])
    #looping over each day
    for i in range(1,days):
        #probabilty of news each day 1%
        news_today = rng.choice([True, False], p = [0.01, 0.99])
        #randomly generated the event to last between 3 to 14 days, if it happens
        if news_today:
            duration = rng.integers(3, 14)
        #looping over each company
        for j in range(n):
            sd = volatility[j]**2
            #increment with normal distrubtuion(0,volatility^2)
            inc = rng.normal(0, sd)
            if news_today == True:
                #m with normal distrubution(0,4)
                m = rng.normal(0, 4)
                #looping over all the days the event happens
                for k in range(i, i + duration):
                    #add drift to any previous drift
                    drift[k][j] += m * volatility[j]
            #calucating the stock price for each stock on that day, with increment and drift added.
            stock_prices[i][j] = stock_prices[i-1][j] + inc + drift[i][j]
            #if stock price is less than 0, it is set to NaN
            if stock_prices[i][j] < 0:
                stock_prices[i][j] = np.nan
    return stock_prices

def get_data(method='read', initial_price=None, volatility=None):
    '''
    Generates or reads simulation data for one or more stocks over 5 years,
    given their initial share price and volatility.

    Input:
        method (str): either 'generate' or 'read' (default 'read').
            If method is 'generate', use generate_stock_price() to generate
                the data from scratch.
            If method is 'read', use Numpy's loadtxt() to read the data
                from the file stock_data_5y.txt.

        initial_price (list): list of initial prices for each stock (default None)
            If method is 'generate', use these initial prices to generate the data.
            If method is 'read', choose the column in stock_data_5y.txt with the closest
                starting price to each value in the list, and display an appropriate message.

        volatility (list): list of volatilities for each stock (default None).
            If method is 'generate', use these volatilities to generate the data.
            If method is 'read', choose the column in stock_data_5y.txt with the closest
                volatility to each value in the list, and display an appropriate message.

        If no arguments are specified, read price data from the whole file.

    Output:
        sim_data (ndarray): NumPy array with N columns, containing the price data
            for the required N stocks each day over 5 years.
    '''

    if method == 'read':
        if initial_price == None:
            if volatility == None:
                sim_data = np.loadtxt('stock_data_5y.txt')
                #delete volatility (first row) from array
                sim_data = np.delete(sim_data,0,0)
                print('Whole file data has been returned.')
                print('Please specify an initial_price if you wish for something more specific.')
                return sim_data
            else:
                #number of stocks needed
                n = len(volatility)
                file_array = np.loadtxt('stock_data_5y.txt')
                m = len(file_array)
                #creating a array based on the length of the volatility and given file
                sim_data = np.zeros((m,n))
                for i in range(n):
                    #getting the index of the array, which is the closest match to the volatility's given
                    index = (np.abs(file_array[0] - volatility[i])).argmin()
                    sim_data[:,i] = file_array[:,index]
                print(f'Found data with initial prices: {sim_data[1]} and volatilities: {sim_data[0]}')
                #delete volatility (first row) from array
                sim_data = np.delete(sim_data, 0, 0)
                return sim_data
        else:
            if volatility == None:
                n = len(initial_price)
                file_array = np.loadtxt('stock_data_5y.txt')
                m = len(file_array)
                sim_data = np.zeros((m,n))
                for i in range(n):
                    #getting the index of the array, which is the closest match to the inital price's given
                    index = (np.abs(file_array[1] - initial_price[i])).argmin()
                    sim_data[:,i] = file_array[:,index]
                print(f'Found data with initial prices: {sim_data[1]} and volatilities: {sim_data[0]}')
                #delete volatility (first row) from array
                sim_data = np.delete(sim_data, 0, 0)
                return sim_data
            else:
                n = len(initial_price)
                file_array = np.loadtxt('stock_data_5y.txt')
                m = len(file_array)
                sim_data = np.zeros((m,n))
                for i in range(n):
                    #getting the index of the array, which is the closest match to the inital price's given
                    index = (np.abs(file_array[1] - initial_price[i])).argmin()
                    sim_data[:,i] = file_array[:,index]
                print(f'Found data with initial prices: {sim_data[1]} and volatilities: {sim_data[0]}.')
                print('Input argument volatility ignored.')
                #delete volatility (first row) from array
                sim_data = np.delete(sim_data, 0, 0)
                return sim_data
    if method == 'generate':
        if initial_price == None:
            if volatility == None:
                print('Please specify the inital price and the volatility.')
                return None
            else:
                print('Please specify the initial price.')
                return None
        else:
            if volatility == None:
                print('Please specify the volatility.')
                return None
            else:
                sim_data = generate_stock_price(1825, initial_price, volatility) #1825 is 5 years in days
                print(f'Data has been generated using initial prices: {initial_price} and volatilities: {volatility}')
                return sim_data
    if method != 'generate' and method != 'read':
        print('Please enter a method: generate or read')
        return None
