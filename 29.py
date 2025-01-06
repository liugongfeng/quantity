'''backtest
start: 2019-01-01 00:00:00
end: 2021-01-01 00:00:00
period: 1m
basePeriod: 1m
balance: 10000
slipPoint: 1
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

from fmz import *
import time

mp = on_line = under_line = 0
up = 1
down = 1

def can_time(hour, miniute):
    hour = str(hour)
    miniute = str(miniute)
    if len(miniute) == 1:
        miniute = '0' + miniute
    return int(hour + miniute)  

def onTick():
    _C(exchange.SetContractType, "TA888")
    bar_arr = _C(exchange.GetRecords)
    if len(bar_arr) < 10:
        return
    
    time_new = bar_arr[-1]['Time']
    time_local_new = time.localtime(time_new / 1000)
    hour_new = int(time.strftime('%H', time_local_new))	
    miniute_new = int(time.strftime('%M', time_local_new))
    day_new = int(time.strftime('%d', time_local_new))
    time_previous = bar_arr[-2]['Time']
    previous = time.localtime(time_previous / 1000)
    day_previous = int(time.strftime('%d', previous))
    global mp, on_line, under_line
    high = bar_arr[-2]['High']
    low = bar_arr[-2]['Low']
    if day_new != day_previous:
        on_line = high * up
        under_line = low * down
    can_trade = can_time(hour_new, miniute_new)
    if can_trade < 930:
        if high > on_line:
            on_line = high * up
        if low < under_line:
            under_line = low * down
    if on_line - under_line < 10:
        return
    
    close_new = bar_arr[-1]['Close']

    if mp > 0 and (close_new < under_line or can_trade > 1450):
        exchange.SetDirection("closebuy")
        exchange.Sell(close_new -1 , 1)
        mp = 0

    if mp < 0 and (close_new > on_line or can_trade > 1450):
        exchange.SetDirection("closesell")
        exchange.Buy(close_new, 1)
        mp = 0

    if mp ==0 and 930 < can_trade < 1450:
        if close_new > on_line:
            exchange.SetDirection("buy")
            exchange.Buy(close_new, 1)
            mp = 1
        elif close_new < under_line:
            exchange.SetDirection("sell")
            exchange.Sell(close_new - 1, 1)
            mp = -1

def main():
    while True:
        onTick()
        Sleep(1000)

task = VCtx(__doc__)
try:
    main()
except :
    task.Show()
