import pandas as pd
import numpy as np
import datetime
from pandas_datareader import data
import matplotlib.pyplot as plt
import json
import time


start = datetime.datetime(2012, 1, 1)
end = datetime.datetime(2017, 12, 30)

symbols = ['^IBEX', 'SAN.MC', 'IDR.MC', 'TL5.MC', 'A3M.MC', 'MEL.MC', 'IAG.MC', 'SAB.MC', 'REP.MC', 'GAS.MC', 'POP.MC', 'GAM.MC', 'ACX.MC', 'BKIA.MC', 'TEF.MC', 'AMS.MC', 'ABE.MC', 'MAP.MC', 'FER.MC', 'BKT.MC', 'ITX.MC', 'GRF.MC', 'TRE.MC', 'CABK.MC', 'AENA.MC', 'MRL.MC', 'DIA.MC', 'REE.MC', 'ELE.MC', 'ANA.MC', 'BBVA.MC', 'VIS.MC', 'ACS.MC', 'CLNX.MC', 'ENG.MC', 'IBE.MC', 'FCC.MC', 'MTS.MC']
our_symbols = {'^IBEX':'IBEX35', 'IDR.MC':'IDR', 'A3M.MC':'A3M', 'MEL.MC':'MEL', 'IAG.MC':'IAG', 'SAN.MC':'SAN', 'GAS.MC':'GAS', 'REP.MC':'REP', 'SAB.MC':'SAB', 'BKIA.MC':'BKIA', 'POP.MC':'POP', 'GAM.MC':'GAM', 'ACX.MC':'ACX', 'TEF.MC':'TEF', 'AMS.MC':'AMS', 'ABE.MC':'ABE', 'MAP.MC':'MAP', 'FER.MC':'FER', 'BKT.MC':'BKT', 'ITX.MC':'ITX', 'GRF.MC':'GRF', 'TRE.MC':'TRE', 'CABK.MC':'CABK', 'AENA.MC':'AENA', 'MRL.MC':'MRL', 'DIA.MC':'DIA', 'REE.MC':'REE', 'ELE.MC':'ELE', 'ANA.MC':'ANA', 'BBVA.MC':'BBVA', 'VIS.MC':'VIS', 'ACS.MC':'ACS', 'CLNX.MC':'CLNX', 'ENG.MC':'ENG', 'IBE.MC':'IBE', 'FCC.MC':'FCC', 'MTS.MC':'MTS', 'TL5.MC':'TL5'}

def get_key(key):
    return our_symbols.get(key)
symbols = sorted(symbols, key=get_key)

adj_close = data.DataReader(symbols, 'yahoo', start, end)['Close']
adj_close = adj_close.ffill()
rets = adj_close.pct_change()
corr = rets.corr()
cols = []
for i in range(len(corr.columns)):
    cols.append(get_key(corr.columns[i]))

plt.figure(1)
plt.imshow(corr, cmap='hot', interpolation='none')
plt.colorbar()
plt.xticks(range(len(corr)), cols, rotation=45)
plt.yticks(range(len(corr)), cols)

plt.figure(2)
plt.scatter(rets.mean(), rets.std())
plt.xlabel('Beneficio')
plt.ylabel('Variabilidad')
for label, x, y in zip(cols, rets.mean(), rets.std()):
    plt.annotate(
        label, 
        xy = (x, y), xytext = (20, -20),
        textcoords = 'offset points', ha = 'right', va = 'bottom',
        bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5),
        arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

plt.show()
