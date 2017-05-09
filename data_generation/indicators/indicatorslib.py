import pandas as pd
import numpy as np

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

def alternation(diffs):
    count = 0
    for i in range(len(diffs)):
        if i > 0 and ((diffs[i] > 0 and diffs[i-1] <= 0) or (diffs[i] < 0 and diffs[i-1] >= 0)):
            count = count + 1
    return (count * 100)/(len(diffs) - 1)

def atr(dataframe):
    shifted = dataframe['Close'].shift()
    dataframe['ATR1'] = abs(dataframe['High'] - dataframe['Low'])
    dataframe['ATR2'] = abs(dataframe['High'] - shifted)
    dataframe['ATR3'] = abs(dataframe['Low'] - shifted)
    dataframe['TrueRange'] = dataframe[['ATR1', 'ATR2', 'ATR3']].max(axis=1)
    dataframe['ATR'] = dataframe['TrueRange']
    dataframe['ATR'].values[0] = np.mean(dataframe['ATR'].values[0:14])
    for i in range(len(dataframe['ATR'].values)):
        if i > 0:
            dataframe['ATR'].values[i] = (dataframe['ATR'].values[i-1] * 13 + dataframe['ATR'].values[i]) / 14
    return dataframe        
