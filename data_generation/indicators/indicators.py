import pandas as pd
import numpy as np
import datetime
from pandas_datareader import data
import json
import requests
import configparser
import indicatorslib as ind

def parse_config():
    config = configparser.ConfigParser()
    config.read('config.cfg')
    url = config['storage'].get('url')
    user = config['storage'].get('user')
    pwd = config['storage'].get('pwd')
    symbols = []
    mapped_symbols = {}
    splits = {}
    
    for section in config.sections():
        if section.startswith('index.'):
            symbols.append(config[section].get('symbol'))
            mapped_symbols[config[section].get('symbol')] = config[section].get('index')
            
            s_symbols = config[section].get('symbols')
            for s in s_symbols.split('\n'):
                current_s = s.split(' ')
                symbols.append(current_s[0])
                mapped_symbols[current_s[0]] = current_s[1]

    for spl in config['splits']:
        print(spl)
                
    def get_key(key):
        return mapped_symbols.get(key)
    symbols = sorted(symbols, key=get_key)
    
    return {
        'url' : url,
        'user' : user,
        'pwd' : pwd,
        'symbols' : symbols,
        'mapped_symbols' : mapped_symbols
        }
    

start = datetime.datetime(2012, 1, 1)
end = datetime.datetime(2017, 12, 31)

conf = parse_config()

stock = data.DataReader('^ibex', 'yahoo', start, end)
stdvp_ibex = np.std(stock['Close'].pct_change().dropna().values[-200:]) * 100
closes = data.DataReader(conf['symbols'], 'yahoo', start, end)['Close']
closes = closes.ffill()
rets = closes.pct_change()
corr = rets.corr()

json_result = []
html_result = '<html><head><title>IBEX 35 Indicators</title><meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no"><link rel="stylesheet" type="text/css" href="bootstrap/css/bootstrap.min.css"><link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/v/dt/jqc-1.12.4/dt-1.10.15/datatables.min.css"/><script type="text/javascript" src="https://cdn.datatables.net/v/dt/jqc-1.12.4/dt-1.10.15/datatables.min.js"></script><script type="text/javascript">$(document).ready(function() {$("#datos").DataTable({"pageLength": 50});} );</script></head><body><div class="container"><div class="page-header"><h1>Indicators <small>' + stock.index[-1].strftime("%a, %d %b %Y") + '</small></h1></div><div class="table-responsive"><table id="datos" class="table table-striped table-bordered table-hover table-condensed"><thead><tr><tr><th>Symbol</th><th>Close</th><th>%</th><th>RSI</th><th>GR20</th><th>GR70</th><th>GR200</th><th>Alter. %</th><th>Beta</th><th>ATR</th><th>Vol. %</th><th>Vol. &euro;</th></tr></thead><tbody>'

s = requests.Session()

for symbol in conf['symbols']:
    stock = data.DataReader(symbol, 'yahoo', start, end)

    ind.atr(stock)

    diffs = np.diff(stock['Close'].values)
    diffs = np.insert(diffs, 0,  0)
    dffis_20 = diffs[-20:]
    dffis_70 = diffs[-70:]
    dffis_200 = diffs[-200:]

    alternation_data = [ind.alternation(dffis_20), ind.alternation(dffis_70), ind.alternation(dffis_200)]
    rsi_data = ind.rsi(stock['Close'], 14)
    ratio_gr_20 = abs(dffis_20[dffis_20 >= 0].sum() / dffis_20[dffis_20 < 0].sum())
    ratio_gr_70 = abs(dffis_70[dffis_70 >= 0].sum() / dffis_70[dffis_70 < 0].sum())
    ratio_gr_200 = abs(dffis_200[dffis_200 >= 0].sum() / dffis_200[dffis_200 < 0].sum())
    stdv = np.std(dffis_200)
    stdvp = np.std(stock['Close'].pct_change().dropna().values[-200:]) * 100
    percent = (stock['Close'].values[-1] / stock['Close'].values[-2]) * 100 - 100
    beta = corr[symbol]['^IBEX'] * (stdvp / stdvp_ibex)

    json_data = {
        'market' : 'IBEX',
        'stock' : conf['mapped_symbols'].get(symbol),
        'date_update' : stock.index[-1].isoformat(),
        'chart_time_period' : 'daily',
        'price' : stock['Close'].values[-1],
        'percent' : percent,
        'indicators' : {
            'rsi' : rsi_data[-1],
            'ratio_gr' : [ratio_gr_20, ratio_gr_70, ratio_gr_200],
            'bar_alternation' : alternation_data,
            'stddev' : stdv,
            'stddevp' : stdvp,
            'atr' : stock['ATR'].values[-1],
            'beta' : beta
            }
        }

    json_result.append(json_data)

    html_result = html_result + ('<tr><td><b>{:s}</b></td><td>{:10.2f}</td><td style="color:' + ('green' if percent >= 0 else 'red') + '">{:10.2f}</td><td>{:10.2f}</td><td>{:10.2f}</td><td>{:10.2f}</td><td>{:10.2f}</td><td>{:10.2f}</td><td>{:10.2f}</td><td>{:10.2f}</td><td>{:10.2f}</td><td>{:10.2f}</td></tr>').format(conf['mapped_symbols'].get(symbol), stock['Close'].values[-1], percent, rsi_data[-1], ratio_gr_20, ratio_gr_70, ratio_gr_200, alternation_data[0], beta, stock['ATR'].values[-1], stdvp, stdv)

html_result = html_result + '</tbody></table></div><div class="panel text-center"><small>StockBros &copy; Ju &amp; Pin</small></div></div></body></html>'
    
with open('results/indicators.json', 'w', encoding='utf8') as json_file:
    json.dump(json_result, json_file, indent=2)
with open('results/indicators.html', 'w', encoding='utf8') as html_file:
    html_file.write(html_result)

r = s.put(conf['url'], verify=False, json=json_result, auth=(conf['user'], conf['pwd']))
print(r.status_code)
