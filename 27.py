'''backtest
start: 2019-01-01 00:00:00
end: 2024-12-18 15:00:00
period: 1d
basePeriod: 1d
balance: 100000
slipPoint: 2
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

from fmz import *
import talib
import numpy as np

mp = 0

def get_data(bars):
    arr = [[], [], []]
    for bar in bars:
        arr[0].append(bar['High'])
        arr[1].append(bar['Low'])
        arr[2].append(bar['Close'])
    return arr


def onTick():
    _C(exchange.SetContractType, "FG000")
    bars = _C(exchange.GetRecords)
    if len(bars) < 100:
        return 

    macd = TA.MACD(bars, 5, 50, 15)
    dif = macd[0][-2]
    dea = macd[1][-2]
    np_arr = np.array(get_data(bars))
    adx_arr = talib.ADX(np_arr[0], np_arr[1], np_arr[2], 14)
    adx1 = adx_arr[-2]
    adx2 = adx_arr[-3]
    last_close = bars[-1]['Close']
    global mp
    if mp == 1 and dif < dea:
        exchange.SetDirection('closebuy')
        exchange.Sell(last_close - 1, 1)
        mp = 0
    if mp == -1 and dif > dea:
        exchange.SetDirection("closesell")
        exchange.Buy(last_close, 1)
        mp = 0
    if mp == 0 and dif > dea and adx1 > adx2:
        exchange.SetDirection("buy")
        exchange.Buy(last_close, 1)
        mp = 1
    if mp == 0 and dif < dea and adx1 > adx2:  
        exchange.SetDirection("sell")
        exchange.Sell(last_close - 1, 1)
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

