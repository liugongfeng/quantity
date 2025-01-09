'''backtest
start: 2019-01-01 00:00:00
end: 2021-01-01 00:00:00
period: 1d
basePeriod: 1d
balance: 10000
slipPoint: 2
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

from fmz import *
up_line = 0
under_line = 0
mp = 0

def onTick():
    exchange.SetContractType('c000')
    bars = exchange.GetRecords()
    if len(bars) < 100:
        return 
    close0 = bars[-1].Close
    high0 = bars[-1].High
    high1 = bars[-2].High
    low0 = bars[-1].Low
    low1 = bars[-2].Low
    highs = TA.Highest(bars, 100, 'High')
    lows = TA.Lowest(bars, 100, 'Low')
    global up_line, under_line, mp
    if high0 > high1:
        up_line = lows
    if low0 < low1:
        up_line = highs
    middle_line = (lows + highs) / 2

    if mp == 0 and close0 > up_line:
        exchange.SetDirection("buy")
        exchange.Buy(close0, 1)
        mp = 1
    if mp == 0 and close0 < under_line:
        exchange.SetDirection("sell")
        exchange.Sell(close0 - 1, 1)
        mp = -1
    if mp > 0 and close0 < middle_line:
        exchange.SetDirection("closebuy")
        exchange.Sell(close0 - 1, 1)
        mp = 0
    if mp < 0 and close0 > middle_line:
        exchange.SetDirection("closesell")
        exchange.Buy(close0, 1)
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