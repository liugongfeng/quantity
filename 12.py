'''backtest
start: 2023-01-01 00:00:00
end: 2024-12-28 15:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"},{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

def on_tick(symbol, ticker):
    Log("symbol: ", symbol, "update")
    Log("ticker: ", ticker)

def on_order(order):
    Log("order update", order)

def main():
    while not exchange.IO("status"):
        Sleep(10)
    exchange.IO("mode", 0)
    _C(exchange.SetContractType, "MA888")
    while True:
        e = exchange.IO("wait")
        if e:
            if e.Event == "tick":
                on_tick(e['Symbol'], e['Ticker'])
            elif e.Event == 'order':
                on_order(e['Order'])
