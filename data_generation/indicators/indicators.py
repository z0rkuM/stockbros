import pandas as pd
import numpy as np
import datetime
from pandas_datareader import data
import matplotlib.pyplot as plt
import json

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
            

start = datetime.datetime(2014, 1, 1)
end = datetime.datetime(2017, 12, 30)

symbols = ['^IBEX', 'SAN.MC', 'SAB.MC', 'POP.MC', 'GAM.MC', 'ACX.MC', 'TEF.MC', 'AMS.MC', 'ABE.MC', 'MAP.MC', 'FER.MC', 'BKT.MC', 'ITX.MC', 'GRF.MC', 'TRE.MC', 'CABK.MC', 'AENA.MC', 'MRL.MC', 'DIA.MC', 'REE.MC', 'ELE.MC', 'ANA.MC', 'BBVA.MC', 'VIS.MC', 'ACS.MC', 'CLNX.MC', 'ENG.MC', 'IBE.MC', 'FCC.MC', 'MTS.MC']
our_symbols = {'^IBEX':'IBEX35', 'SAN.MC':'SAN', 'SAB.MC':'SAB', 'POP.MC':'POP', 'GAM.MC':'GAM', 'ACX.MC':'ACX', 'TEF.MC':'TEF', 'AMS.MC':'AMS', 'ABE.MC':'ABE', 'MAP.MC':'MAP', 'FER.MC':'FER', 'BKT.MC':'BKT', 'ITX.MC':'ITX', 'GRF.MC':'GRF', 'TRE.MC':'TRE', 'CABK.MC':'CABK', 'AENA.MC':'AENA', 'MRL.MC':'MRL', 'DIA.MC':'DIA', 'REE.MC':'REE', 'ELE.MC':'ELE', 'ANA.MC':'ANA', 'BBVA.MC':'BBVA', 'VIS.MC':'VIS', 'ACS.MC':'ACS', 'CLNX.MC':'CLNX', 'ENG.MC':'ENG', 'IBE.MC':'IBE', 'FCC.MC':'FCC', 'MTS.MC':'MTS'}

json_result = []
html_result = '<html><head><title>IBEX 35 Indicators</title><style>td, th {padding:3px 10px; text-align:left} body {font-family:arial}</style></head><body><table><thead><tr><tr><th>Symbol</th><th>Close</th><th>RSI</th><th>Ratio GR 20-70-200</th><th>Alternation 20-70-200</th></tr></tr></thead><tbody>'

for symbol in symbols:
    stock = data.DataReader(symbol, 'yahoo', start, end)

    diffs = np.diff(stock['Close'].values)
    diffs = np.insert(diffs, 0,  0)
    dffis_20 = diffs[-20:]
    dffis_70 = diffs[-70:]
    dffis_200 = diffs[-200:]

    alternation_20 = alternation(dffis_20)
    alternation_70 = alternation(dffis_70)
    alternation_200 = alternation(dffis_200)
    rsi_data = rsi(stock['Close'], 14)
    ratio_gr_20 = len(dffis_20[dffis_20 >= 0]) / len(dffis_20[dffis_20 < 0])
    ratio_gr_70 = len(dffis_70[dffis_70 >= 0]) / len(dffis_70[dffis_70 < 0])
    ratio_gr_200 = len(dffis_200[dffis_200 >= 0]) / len(dffis_200[dffis_200 < 0])

    json_result.append({
        'market' : 'IBEX',
        'stock' : our_symbols.get(symbol),
        'date_update' : stock.index[-1].isoformat(),
        'chart_time_period' : 'daily',
        'price' : stock['Close'].values[-1],
        'indicators' : {
            'rsi' : rsi_data[-1],
            'ratio_gr' : [ratio_gr_20, ratio_gr_70, ratio_gr_200],
            'bar_alternation' : [alternation_20, alternation_70, alternation_200]
            }
        })

    html_result = html_result + '<tr><td>{:s}</td><td>{:10.3f}</td><td>{:10.2f}</td><td>{:10.2f} - {:10.2f} - {:10.2f}</td><td>{:10.2f} - {:10.2f} - {:10.2f}</td></tr>'.format(our_symbols.get(symbol), stock['Close'].values[-1], rsi_data[-1], ratio_gr_20, ratio_gr_70, ratio_gr_200, alternation_20, alternation_70, alternation_200)

html_result = html_result + '</tbody></table></body></html>'
    
with open('indicators.json', 'w', encoding='utf8') as json_file:
    json.dump(json_result, json_file, indent=2)
with open('indicators.html', 'w', encoding='utf8') as html_file:
    html_file.write(html_result)
