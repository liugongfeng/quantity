'''backtest
start: 2019-01-01 00:00:00
end: 2021-01-01 00:00:00
period: 5m
basePeriod: 5m
balance: 10000
slipPoint: 1
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

from fmz import *
up_line = down_line = trade_count = 0

def current_time():
    current = bar_arr[-1]['Time']
    time_local = time.localtime(current / 1000)
    hour = time.strftime("%H", time_local)	
    minute = time.strftime("%M", time_local)
    if len(minute) == 1:
        minute = '0' + minute
    return int(hour + minute)


def onTick():
    _C(exchange.SetContractType, "TA888")
    bar_arr = _C(exchange.GetRecords)
    current_close = bar_arr[-1]['Close']
    global up_line, down_line, trade_count
    current = current_time(bar_arr)
    if current == 930:
        bar_arr = _C(exchange.GetRecords, PERIOD_D1)
        up_line = bar_arr[-1]['High']
        down_line = bar_arr[-1]['Low']
        trade_count = 0
    position_arr = _C(exchange.GetPosition)
    if len(position_arr) > 0:
        position_arr = position_arr[0]
        if position_arr['ContractType'][:2] == 'TA':
            if position_arr['Type'] % 2 == 0:
                position = position_arr['Amount']
            else:
                position = -position_arr['Amount']
            profit = position_arr['Profit']
    else:
        position = 0
        profit = 0

    if current > 1450 or profit > 500 * 3 or profit < -500:
        if position > 0:
            exchange.SetDirection("closebuy")
            exchange.Sell(current_close - 1, 1)
        elif position < 0:
            exchange.SetDirection("closesell")
            exchange.Buy(current_close + 1, 1)
        return
    
    if position == 0 and trade_count < 3 and 930 < current < 1450:
        if current_close > up_line:
            exchange.SetDirection("buy")
            exchange.Buy(current_close + 1, 1)
            trade_count += 1
        elif current_close < down_line:
            exchange.SetDirection("sell")
            exchange.Sell(current_close - 1, 1)
            trade_count += 1

def main():
    while True:
        onTick()
        Sleep(1000) 

task = VCtx(__doc__)
try:
    main()
except:
    task.Show()