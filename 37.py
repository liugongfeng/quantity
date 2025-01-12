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

def onTick():
    exchange.SetContractType('rb000')
    bar_arr = exchange.GetRecords()
    if len(bar_arr) < 100:
        return
    close0 = bar_arr[-1]['Close']
    bar_arr.pop()
    close1 = bar_arr[-1]['Close']
    close30 = bar_arr[-30]['Close']
    hh30 = TA.Highest(bar_arr, 30, 'High')
    ll30 = TA.Lowest(bar_arr, 30, 'Low')
    cmi = abs((close1 - close30) / (hh30 - ll30))
    high1 = bar_arr[-1]['High']
    low1 = bar_arr[-1]['Low']
    kod = (close1 + high1 + low1) / 3
    if close1 > kod:
        be = 1
        se = 0
    else:
        be = 0
        se = 1
    atr10 = TA.ATR(bar_arr, 10)[-1]
    high2 = bar_arr[-2]['High']
    high3 = bar_arr[-3]['High']
    low2 = bar_arr[-2]['Low']
    low3 = bar_arr[-3]['Low']
    avg3high = (high1 + high2 + high3) / 3
    avg3low = (low1 + low2 + low3) / 3 

    open1 = bar_arr[-1]['Open']
    if close1 > kod:
        lep = open1 + atr10 * 3
        sep = open1 - atr10 * 2
    else:
        lep = open1 + atr10 * 2
        sep = open1 - atr10 * 3
    lep1 = max(lep, avg3high)
    sep1 = min(sep, avg3low)
    boll = TA.BOLL(bar_arr, 50, 2)
    up_line = boll[0][-1]
    mid_line = boll[1][-1]
    down_line = boll[2][-1]
    global mp
    if cmi < 20:
        if mp == 0 and close1 >= lep1 and se:
            exchange.SetDirection("buy")
            exchange.Buy(close0, 1)
            mp = 1
        if mp == 0 and close1 <= sep1 and be:
            exchaneg.SetDirection("sell")
            exchange.Sell(close0 - 1, 1)
            mp = -1
        if mp == 1 and (close1 >= avg3high or be):
            exchange.SetDirection("closebuy")
            exchange.Sell(close0 - 1, 1)
            mp = 0
        if mp == -1 and (close1 <= avg3low or se):
            exchange.SetDirection("closesell")
            exchange.Buy(close0, 1)
            mp = 0
    else:
        if mp == 0 and close1 >= up_line:
            exchange.SetDirection("buy")
            exchange.Buy(close0, 1)
            mp = 1
        if mp == 0 and close1 <= down_line:
            exchange.SetDirection("sell")
            exchange.Sell(close0 - 1, 1)
            mp = -1
        if mp == 1 and close1 <= mid_line:
            exchange.SetDirection("closebuy")
            exchange.Sell(close0 - 1, 1)
            mp = 0
        if mp == -1 and close1 >= mid_line:
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
