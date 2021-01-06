# Evaluate performance.
import pandas as pd
import numpy as np

def read_ledger(ledger_file):
    '''
    Reads and reports useful information from ledger_file.

    Input:

    Output: profit (float): Returns profit for graph building.
    '''
    #To show which file the below results refer to
    print(f'{ledger_file}:')
    #putting the file into a dataframe
    header_list = ['type','day','stock','num_shares','price','fees','total']
    df = pd.read_csv(ledger_file, names=header_list)
    #total transactions
    total_t = len(df)
    #total number of buys and sells
    total_bs = df['type'].value_counts()
    total_b = total_bs['buy']
    #in case there are zero sales
    try:
        total_s = total_bs['sell']
    except:
        total_s = 0
    #total amount brought and sold
    a_buy = df.loc[df['type'] == 'buy', 'total']
    a_sell = df.loc[df['type'] == 'sell', 'total']
    #total profit
    profit = round(sum(a_buy) + sum(a_sell),2)
    #average/worst/best stock
    if len(df.stock.unique()) > 1:
        s_t = []
        for i in range(len(df.stock.unique())):
            s_t.append(sum(df.loc[df['stock'] == i, 'total']))
        max_s_t = round(max(s_t),2)
        min_s_t = round(min(s_t),2)
        avg_s_t = round(np.average(s_t),2)
        print(f'The worst performing stock made a profit/loss of {min_s_t}')
        print(f'The best performing stock made a profit/loss of {max_s_t}')
        print(f'Average stock profit/loss was {avg_s_t}')

    print(f'Total profit: {profit}')
    print(f'Total transactions: {total_t}, split between {total_b} buys and {total_s} sells\n')

    return profit
