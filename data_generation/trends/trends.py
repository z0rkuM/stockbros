import pandas as pd
import numpy as np
import datetime
from pandas_datareader import data
import matplotlib.pyplot as plt

def rsi(close, window_length):
    delta = close.diff()[1:]
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    roll_up1 = pd.stats.moments.ewma(up, window_length)
    roll_down1 = pd.stats.moments.ewma(down.abs(), window_length)
    RS1 = roll_up1 / roll_down1
    RSI1 = 100.0 - (100.0 / (1.0 + RS1))

    return RSI1

def momentum(close, window_length):
    return close.diff(window_length)

umbral = 0.0025
start = datetime.datetime(2012, 1, 1)
end = datetime.datetime(2017, 12, 30)
stock = data.DataReader('^IBEX', 'yahoo', start, end)

stock['20d_ma'] = stock['Close'].rolling(window=20,center=False).mean()

#stock = stock.reset_index()

diffs = np.diff(stock['Close'].values)
diffs = np.insert(diffs, 0,  0)

my_data = []
wv_data = []
v_weights = ((stock['Volume'].values - (stock['Volume'].rolling(window=20,center=False).mean()).values) / (stock['Volume'].rolling(window=20,center=False).mean()).values) * 0.1

for i in range(len(diffs)) :
    if i==0:
        my_data.append(stock['Close'].values[0])
        
    elif diffs[i] == 0 or (abs(diffs[i]) / stock['Close'].values[i-1]) <= umbral:
        if i > 1:
            if (stock['High'].values[i] - stock['Close'].values[i]) > (stock['Close'].values[i] - stock['Low'].values[i]):
                my_data.append(stock['High'].values[i])
            else:
                my_data.append(stock['Low'].values[i])
        else:
            my_data.append(my_data[i-1])
        
    elif diffs[i] < 0:
        if i > 1 and my_data[i-1] > my_data[i-2] and stock['High'].values[i] > my_data[i-1]:
            my_data.append(stock['High'].values[i])
        else:
            my_data.append(stock['Low'].values[i])
            
    else:
        if i > 1 and my_data[i-1] < my_data[i-2] and stock['Low'].values[i] < my_data[i-1]:
            my_data.append(stock['Low'].values[i])
        else:    
            my_data.append(stock['High'].values[i])


my_data = np.array(my_data)

for i in range(len(diffs)) :
    if i==0:
        wv_data.append(my_data[0])
    elif diffs[i] < 0:
        wv_data.append(my_data[i] - v_weights[i] * my_data[i])
    elif diffs[i] >= 0:
        wv_data.append(my_data[i] + v_weights[i] * my_data[i])
        
pivots = (stock['High'].values + stock['Close'].values + stock['Low'].values ) / 3

stock['trends'] = my_data
stock['wv_trends'] = wv_data
stock['diffs'] = wv_data - my_data

plt.subplot(311)
stock['trends'].plot(color='black', linewidth=.75)
#stock['wv_trends'].plot(color='red', linewidth=.5)
#plt.plot(stock['Date'].values, (pd.Series(wv_data).rolling(window=20,center=False).mean()).values, color='red')
#plt.plot(stock['Date'].values, (pd.Series(wv_data).ewm(span=20).mean()).values, color='blue')

plt.subplot(312)
#stock['Volume'].plot(linewidth=.75)
stock['Volume'].rolling(window=7,center=False).mean().plot(color='green', linewidth=.5)
stock['Volume'].rolling(window=20,center=False).mean().plot(color='red', linewidth=.5)

plt.subplot(313)
stock['rsiToplimit'] = 100 * np.ones(len(stock['trends']))
stock['rsiBotlimit'] = 0 * np.ones(len(stock['trends']))
#rsi(stock['trends'], 14).plot(color='green', linewidth=.5)
#rsi(stock['trends'], 3).rolling(window=12,center=False).mean().plot(color='red', linewidth=.5)

ci = (rsi(stock['trends'], 3).rolling(window=3,center=False).mean() + momentum(rsi(stock['trends'], 14), 9))
ci.plot(color='red', linewidth=.5)
ci.rolling(window=13,center=False).mean().plot(color='green', linewidth=.5)
ci.rolling(window=33,center=False).mean().plot(color='blue', linewidth=.5)

stock['rsiToplimit'].plot(color='black', linewidth=.25)
stock['rsiBotlimit'].plot(color='black', linewidth=.25)
#hist_values = wv_data - my_data
#stock['diffs'].rolling(window=7,center=False).mean().plot(kind='bar')
#plt.bar(stock.reset_index()['Date'].values, (pd.Series(hist_values).rolling(window=7,center=False).mean()).values)

plt.show()
