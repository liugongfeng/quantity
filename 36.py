'''backtest
start: 2019-01-01 00:00:00
end: 2021-01-01 00:00:00
period: 1h
basePeriod: 1h
balance: 10000
slipPoint: 2
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"}]
'''
from fmz import *
mp = 0
last_bar_time = 0
up_line = 0
down_line = 0

Ks = 3
Kx = 2
Cycle = 5

def onTick():
    global mp, last_bar_time, up_line, down_line
    exchange.SetContractType('rb000')
    bar_arr = exchange.GetRecords()
    if not bar_arr or len(bar_arr) < 5:
        return
    last_bar = bar_arr[len(bar_arr) - 1]
    last_bar_close = last_bar['Close']
    if last_bar_close != last_bar['Time']:
        hh = TA.Highest(bar_arr, Cycle, 'High')
        hc = TA.Highest(bar_arr, Cycle, 'Close')
        ll = TA.Lowest(bar_arr, Cycle, 'Low')
        lc = TA.Lowest(bar_arr, Cycle, 'Close')
        Range = max(hh - lc, hc - ll)
        up_line = _N(last_bar['Open'] + 3 * Range)
        down_line = _N(last_bar['Open'] - 2 * Range)
        last_bar_time = last_bar['Time']
    if mp == 0 and last_bar_close >= up_line:
        exchange.SetDirection("buy")
        exchange.Buy(last_bar_close, 1)
        mp = 1
    if mp == 0 and last_bar_close <= down_line:
        exchange.SetDirection("sell")
        exchange.Sell(last_bar_close - 1, 1)
        mp = -1
    if mp == 1 and last_bar_close <= down_line:
        exchange.SetDirection("closebuy")
        exchange.Sell(last_bar_close - 1, 1)
        mp = 0
    if mp == -1 and last_bar_close >= up_line:
        exchange.SetDirection("closesell")
        exchange.Buy(last_bar_close, 1)
        mp = 0


def main():
    while True:
        onTick()
        Sleep(1000)

task = VCtx(__doc__)
try:
    main()
except:
    task.Show() 



