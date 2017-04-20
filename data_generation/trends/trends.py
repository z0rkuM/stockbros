import pandas as pd
import numpy as np
import datetime
from pandas_datareader import data
import matplotlib.pyplot as plt

def rsi(close, window_length):
    delta = close.diff()[1:]

    # Make the positive gains (up) and negative gains (down) Series
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    # Calculate the EWMA
    roll_up1 = pd.stats.moments.ewma(up, window_length)
    roll_down1 = pd.stats.moments.ewma(down.abs(), window_length)

    # Calculate the RSI based on EWMA
    RS1 = roll_up1 / roll_down1
    RSI1 = 100.0 - (100.0 / (1.0 + RS1))

    # Calculate the SMA
    roll_up2 = pd.rolling_mean(up, window_length)
    roll_down2 = pd.rolling_mean(down.abs(), window_length)

    # Calculate the RSI based on SMA
    RS2 = roll_up2 / roll_down2
    RSI2 = 100.0 - (100.0 / (1.0 + RS2))

    return RSI2

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
stock['wv_trends'].plot(color='red', linewidth=.5)
#plt.plot(stock['Date'].values, (pd.Series(wv_data).rolling(window=20,center=False).mean()).values, color='red')
#plt.plot(stock['Date'].values, (pd.Series(wv_data).ewm(span=20).mean()).values, color='blue')

plt.subplot(312)
stock['Volume'].plot(linewidth=.75)
stock['Volume'].rolling(window=7,center=False).mean().plot(color='green', linewidth=.5)
stock['Volume'].rolling(window=20,center=False).mean().plot(color='red', linewidth=.5)

plt.subplot(313)
rsi(stock['trends'], 14).plot(color='green', linewidth=.5)
#hist_values = wv_data - my_data
#stock['diffs'].rolling(window=7,center=False).mean().plot(kind='bar')
#plt.bar(stock.reset_index()['Date'].values, (pd.Series(hist_values).rolling(window=7,center=False).mean()).values)

plt.show()
