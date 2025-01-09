'''backtest
start: 2019-01-01 00:00:00
end: 2021-01-01 00:00:00
period: 1d
basePeriod: 1d
slipPoint: 0
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES","balance":500000}]
'''

from fmz import *

def get_position():
    position = 0
    position_arr = _C(exchange.GetPosition)
    if len(position_arr) > 0:
        for i in position_arr:
            if i['ContractType'] [:2] == 'IH':
                if ['Type'] % 2 == 0:
                    positioin = i['Amount']
                else:
                    position = -i['Amount']
    return position

def onTick():
    exchange.SetContractType('IH000')
    bars_arr = exchange.GetRecords()
    if len(bars_arr) < 10:
        return 
    bar1 = bars_arr[-2]
    bar2 = bars_arr[-3]
    mov_mid = (bar1['High'] + bar1['Low']) / 2 - (bar2['High'] + bar2['Low']) / 2
    if bar1['High'] != bar1['Low']:
        ratio = (bar1['Volume'] / 10000) / (bar1['High'] - bar1['Low'])
    else:
        ratio = 0
    if ratio > 0:
        emv = mov_mid / ratio
    else:
        emv = 0
    current_price = bars_arr[-1]['Close']
    position = get_position()
    if position > 0:
        if emv < 0:
            exchange.SetDirection('closebuy')
            exchange.Sell(round(current_price - 1, 2), 1)
    if position < 0:
        if emv > 0:
            exchange.SetDirection('closesell')
            exchange.Buy(round(current_price + 0.8, 2), 1)
    if position == 0:
        if emv > 0:
            exchange.SetDirection('buy')
            exchange.Buy(round(current_price + 0.8, 2), 1)
        if emv < 0:
            exchange.SetDirection('sell')
            exchange.Sell(round(current_price - 1, 2), 1)


def main():
    while True:
        onTick()
        Sleep(1000)

task = VCtx(__doc__)
try:
    main()
except:
    task.Show() 