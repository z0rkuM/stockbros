import pandas as pd
import numpy as np
import datetime
from pandas_datareader import data
import matplotlib.pyplot as plt
import json
import time

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

            

start = datetime.datetime(2012, 1, 1)
end = datetime.datetime(2017, 12, 30)

symbols = ['^IBEX', 'SAN.MC', 'SAB.MC', 'POP.MC', 'GAM.MC', 'ACX.MC', 'TEF.MC', 'AMS.MC', 'ABE.MC', 'MAP.MC', 'FER.MC', 'BKT.MC', 'ITX.MC', 'GRF.MC', 'TRE.MC', 'CABK.MC', 'AENA.MC', 'MRL.MC', 'DIA.MC', 'REE.MC', 'ELE.MC', 'ANA.MC', 'BBVA.MC', 'VIS.MC', 'ACS.MC', 'CLNX.MC', 'ENG.MC', 'IBE.MC', 'FCC.MC', 'MTS.MC']
our_symbols = {'^IBEX':'IBEX35', 'SAN.MC':'SAN', 'SAB.MC':'SAB', 'POP.MC':'POP', 'GAM.MC':'GAM', 'ACX.MC':'ACX', 'TEF.MC':'TEF', 'AMS.MC':'AMS', 'ABE.MC':'ABE', 'MAP.MC':'MAP', 'FER.MC':'FER', 'BKT.MC':'BKT', 'ITX.MC':'ITX', 'GRF.MC':'GRF', 'TRE.MC':'TRE', 'CABK.MC':'CABK', 'AENA.MC':'AENA', 'MRL.MC':'MRL', 'DIA.MC':'DIA', 'REE.MC':'REE', 'ELE.MC':'ELE', 'ANA.MC':'ANA', 'BBVA.MC':'BBVA', 'VIS.MC':'VIS', 'ACS.MC':'ACS', 'CLNX.MC':'CLNX', 'ENG.MC':'ENG', 'IBE.MC':'IBE', 'FCC.MC':'FCC', 'MTS.MC':'MTS'}

def get_key(key):
    return our_symbols.get(key)
symbols = sorted(symbols, key=get_key)

stock = data.DataReader(symbols[0], 'yahoo', start, end)

json_result = []
html_result = '<html><head><title>IBEX 35 Indicators</title><meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"><link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.min.css"><link rel="stylesheet" type="text/css" href="styles.css"></head><body><div class="container"><div class="page-header"><h1>Indicators <small>' + stock.index[-1].strftime("%a, %d %b %Y") + '</small></h1></div><div class="table-responsive"><table class="table table-striped table-bordered table-hover table-condensed"><thead><tr><tr><th>Symbol</th><th>Close</th><th>Change %</th><th>RSI</th><th colspan="3">Ratio GR</th><th colspan="3">Alternation %</th><th>Vol. %</th><th>Vol. &euro;</th></tr></thead><tbody>'

for symbol in symbols:
    stock = data.DataReader(symbol, 'yahoo', start, end)

    diffs = np.diff(stock['Close'].values)
    diffs = np.insert(diffs, 0,  0)
    dffis_20 = diffs[-20:]
    dffis_70 = diffs[-70:]
    dffis_200 = diffs[-200:]

    alternation_data = [alternation(dffis_20), alternation(dffis_70), alternation(dffis_200)]
    rsi_data = rsi(stock['Close'], 14)
    ratio_gr_20 = abs(dffis_20[dffis_20 >= 0].sum() / dffis_20[dffis_20 < 0].sum())
    ratio_gr_70 = abs(dffis_70[dffis_70 >= 0].sum() / dffis_70[dffis_70 < 0].sum())
    ratio_gr_200 = abs(dffis_200[dffis_200 >= 0].sum() / dffis_200[dffis_200 < 0].sum())
    stdv = np.std(dffis_200)
    stdvp = np.std(stock['Close'].pct_change().dropna().values[-200:]) * 100
    percent = (stock['Close'].values[-1] / stock['Close'].values[-2]) * 100 - 100
        
    json_result.append({
        'market' : 'IBEX',
        'stock' : our_symbols.get(symbol),
        'date_update' : stock.index[-1].isoformat(),
        'chart_time_period' : 'daily',
        'price' : stock['Close'].values[-1],
        'percent' : stock['Close'].values[-1],
        'indicators' : {
            'rsi' : rsi_data[-1],
            'ratio_gr' : [ratio_gr_20, ratio_gr_70, ratio_gr_200],
            'bar_alternation' : alternation_data,
            'stddev' : stdv,
            'stddevp' : stdvp
            }
        })

    html_result = html_result + ('<tr><td>{:s}</td><td>{:10.2f}</td><td style="color:' + ('green' if percent >= 0 else 'red') + '">{:10.2f}</td><td>{:10.2f}</td><td>{:10.2f}</td><td>{:10.2f}</td><td>{:10.2f}</td><td>{:10.2f}</td><td>{:10.2f}</td><td>{:10.2f}</td><td>{:10.2f}</td><td>{:10.2f}</td></tr>').format(our_symbols.get(symbol), stock['Close'].values[-1], percent, rsi_data[-1], ratio_gr_20, ratio_gr_70, ratio_gr_200, alternation_data[0], alternation_data[1], alternation_data[2], stdvp, stdv)

html_result = html_result + '</tbody></table></div><div class="panel text-center"><small>StockBros &copy;</small></div></div></body></html>'
    
with open('indicators.json', 'w', encoding='utf8') as json_file:
    json.dump(json_result, json_file, indent=2)
with open('indicators.html', 'w', encoding='utf8') as html_file:
    html_file.write(html_result)
