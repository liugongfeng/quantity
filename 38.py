'''backtest
start: 2020-01-01 00:00:00
end: 2021-01-01 00:00:00
period: 1h
basePeriod: 1h
slipPoint: 2
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES". "balance": 100000}]
'''

from fmz import *

def onTick():
    exchange.SetContractType('rb000')
    bars_arr = exchange.GetRecords()
    if len(bars_arr) < 2:
        return
    yes_open = bars_arr[-2]['Open']
    yes_high = bars_arr[-2]['High']
    yes_low = bars_arr[-2]['Low']
    yes_close = bars_arr[-2]['Close']
    pivot = (yes_high + yes_low + yes_close) / 3
    r1 - 2 * pivot - yes_low
    r2 = pivot + (yes_high - yes_low)
    r3 = yes_high + 2 * (pivot - yes_low)
    s1 = 2 * pivot - yes_high
    s2 = pivot - (yes_high - yes_low)
    s3 = yes_low - 2 * (yes_high - pivot)
    today_high = bars_arr[-1]['High']
    today_low = bars_arr[-1]['Low']
    current_price = _C(exchange.GetTicker).Last

    position_arr = _C(exchange.GetPosition)
    if len(position_arr) > 0:
        for i in position_arr:
            if i['ContractType'][:2] == 'rb':
                if i['Type'] % 2 == 0:
                    position = i['Amount']
                else:
                    position = -i['Amount']
                profit = i['Profit']
    else:
        position = 0
        profit = 0
    if position == 0:
        if current_price > r3 :
            exchange.SetDirection("buy")
            exchange.Buy(current_price +1, 1)
        if current_price < s3:
            exchange.SetDirection("sell")
            exchange.Sell(current_price - 1, 1)
    if position > 0:
        if today_high > r2 and current_price < r1 or current_price < s3:
            exchange.SetDirection("closebuy")
            exchange.Sell(current_price - 1, 1)
            exchange.SetDirection("sell")
            exchange.Sell(current_price - 1, 1)
    if position < 0:
        if today_low < s2 and current_price > s1 or current_price > r3:
            exchange.SetDirection("closesell")
            exchange.Buy(current_price + 1, 1)
            exchange.SetDirection("buy")
            exchange.Buy(current_price + 1, 1)

def main():
    while True:
        onTick()
        Sleep(1000)

task = VCtx(__doc__)
try:
    main()
except:
    task.Show()
