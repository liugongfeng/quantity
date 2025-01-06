'''backtest
start: 2019-01-01 00:00:00
end: 2021-01-01 00:00:00
period: 1d
basePeriod: 1d
balance: 10000
slipPoint: 1
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

from fmz import *
mp = 0

def onTick():
    _C(exchange.SetContractType, "c000")
    bar_arr = _C(exchange.GetRecords)
    if len(bar_arr) < 60:
        return
    close_new = bar_arr[-1]['Close']
    close_last = bar_arr[-2]['Close']
    bar_arr.pop()
    on_line = TA.Highest(bar_arr, 55, 'High')
    under_line = TA.Lowest(bar_arr, 55, 'Low')
    middle_line = (on_line + under_line) / 2
    global mp 
    if mp > 0 and close_new < middle_line:
        exchange.SetDirection("closebuy")
        exchange.Sell(close_new, 1)
        mp = 0
    if mp < 0 and close_new > middle_line:
        exchange.SetDirection("closesell")
        exchange.Buy(close_new, 1)
        mp = 0
    if mp == 0:
        if close_last > on_line:
            exchange.SetDirection("buy")
            exchange.Buy(close_new, 1)
            mp = 1
        elif close_last < under_line:
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
except:
    task.Show()