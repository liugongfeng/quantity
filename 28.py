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
import talib
import numpy as np

mp = 0

def get_close(r):
    arr = []
    for i in r:
        arr.append(i['Close'])
    return arr

def is_cross(arr1, arr2):
    if arr1[-2] < arr2[-2] and arr1[-1] > arr2[-1]:
        return True

def onTick():
    _C(exchange.SetContractType, "rb000")
    bar_arr = _C(exchange.GetRecords)
    if len(bar_arr) < 100:
        return 
    
    close_arr = get_close(bar_arr)
    np_close_arr = np.array(close_arr)
    ama1 = talib.KAMA(np_close_arr, 10).tolist()
    ama2 = talib.KAMA(np_close_arr, 100).tolist()
    last_close = close_arr[-1]
    
    
    global mp
    if mp == 1 and is_cross(ama2, ama1):
        exchange.SetDirection('closebuy')
        exchange.Sell(last_close - 1, 1)
        mp = 0

    if mp == -1 and is_cross(ama1, ama2):
        exchange.SetDirection("closesell")
        exchange.Buy(last_close, 1)
        mp = 0

    if mp == 0 and is_cross(ama1, ama2):
        exchange.SetDirection("buy")
        exchange.Buy(last_close, 1)
        mp = 1

    if mp == 0 and is_cross(ama2, ama1):  
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

