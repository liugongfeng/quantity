'''backtest
start: 2019-01-01 00:00:00
end: 2021-01-01 00:00:00
period: 15m
basePeriod: 15m
slipPoint: 2
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES","balance":100000}]
'''

from fmz import *
import time

mp = 0

def trade_time(hour, minute):
    minute = str(minute)
    if len(minute) == 1:
        minute = '0' + minute
    return int(str(hour) + minute)

def onTick():
    _C(exchange.SetContractType, "ag888")
    bar_arr = _C(exchange.GetRecords, PERIOD_D1)
    if len(bar_arr) < 2:
        return
    yh = bar_arr[-2]['High']
    yl = bar_arr[-2]['Low']
    today_open = bar_arr[-1]['Open']
    bar_arr = _C(exchange.GetRecords)
    current = bar_arr[-1]['Time']
    local = time.localtime(current / 1000)
    hour = int(time.strftime("%H", local))
    minute = int(time.strftime("%M", local))
    price = bar_arr[-1]['Close']
    global mp

    if today_open / yh > 1.005:
        long_stop = yh
    elif today_open / yh < 0.995:
        long_stop = today_open
    else:
        long_stop = (yh + yl) / 2

    if today_open / yl < 0.995:
        short_stop = yl
    elif today_open / yl > 1.005:
        short_stop = today_open
    else:
        short_stop = (yh + yl) / 2

    trading = trade_time(hour, minute)
    if mp > 0:
        if price < long_stop or trading > 1450:
            exchange.SetDirection("closebuy")
            exchange.Sell(price - 1, 1)
            mp = 0
    if mp < 0:
        if price > short_stop or trading > 1450:
            exchange.SetDirection("closesell")
            exchange.Buy(price, 1)
            mp = 0
    if mp == 0 and 930 < trading < 1450:
        if price > yh:
            exchange.SetDirection("buy")
            exchange.Buy(price, 1)
            mp = 1
        elif price < yl:
            exchange.SetDirection("sell")
            exchange.Sell(price - 1, 1)
            mp = -1


def main():
    while True:
        onTick()
        Sleep(1000)

task = VCtx(__doc__)
try:
    main()
except:
    task.Show()