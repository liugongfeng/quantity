'''backtest
start: 2019-01-01 00:00:00
end: 2021-01-01 00:00:00
period: 1d
basePeriod: 1d
slipPoint: 2
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES","balance":100000}]
'''

from fmz import *
import talib
import numpy as np

mp = 0

def get_data(bars):
    arr = [[], []]
    for bar in bars:
        arr[0].append(bar['High'])
        arr[1].append(bar['Low'])
    return arr


def onTick():
    exchange.SetContractType("ni000")
    bars = exchange.GetRecords()
    if len(bars) < 100:
        return
    np_arr = np.array(get_data(bars))
    aroon = talib.AROON(np_arr[0], np_arr[1], 20)
    aroon_up = aroon[1][len(aroon[1]) - 2]
    aroon_down = aroon[0][len(aroon[0]) - 2]
    close0 = bars[len(bars) - 1].Close
    global mp

    if mp == 0 and aroon_up > aroon_down and aroon_up > 50:
        exchange.SetDirection("buy")
        exchange.Buy(close0, 1)
        mp = 1
    if mp == 0 and aroon_down > aroon_up and aroon_down > 50:
        exchange.SetDirection("sell")
        exchange.Sell(close0 - 1, 1)
        mp = -1
    if mp > 0 and (aroon_up < aroon_down or aroon_up < 50):
        exchange.SetDirection("closebuy")
        exchange.Sell(close0 - 1, 1)
        mp = 0
    if mp < 0 and (aroon_down < aroon_up or aroon_down < 50):
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