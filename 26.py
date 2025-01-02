'''backtest
start: 2023-01-01 00:00:00
end: 2024-12-31 15:00:00
period: 1d
basePeriod: 1d
slipPoint: 2
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

from fmz import *

def ontTick():
    _C(exchange.SetContractType, "FG000")
    bar = _C(exchange.GetRecords)
    if len(bar) < 100:
        return 
    macd = TA.MACD(bar, 5, 50, 15)        
    dif = macd[0][-2]
    dea = macd[1][-2]
    last_close = bar[-1]['Close']
    global mp
    if mp == 1 and dif < dea:
        exchange.SetDirection('closebuy')
        exchange.Sell(last_close - 1, 1)
        mp = 0

    if mp == -1 and dif > dea:
        exchange.SetDirection("closesell")
        exchange.Buy(last_close, 1)
        mp = 0

    if mp == 0 and dif > dea:
        exchange.SetDirection("buy")
        exchange.Buy(last_close, 1)
        mp = 1

    if mp == 0 and dif < dea:
        exchange.SetDirection("sell")
        exchange.Sell(last_close - 1, 1)
        mp = -1   


def main():
    while True:
        ontTick()
        Sleep(1000)

task = VCtx(__doc__)
try:
    main()
except:
    task.Show()
