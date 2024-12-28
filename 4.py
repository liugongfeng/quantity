'''backtest
start: 2023-01-01 00:00:00
end: 2024-12-18 15:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"},{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

def main():
    while True:
        if exchange.IO("status"):
            exchange.SetContractType("rb888")
            ticker = exchange.GetTicker()
            depth = exchange.GetDepth()
            trades = exchange.GetTrades()
            records = exchange.GetRecords()
            Log("rb888 ticker last: ", ticker['Last'])
            Log("rb888 depth: ", depth)
            Log("rb888 trades: ", trades)
            Log("rb888 records: ",  records)
            LogStatus(_D(), "Connected! CTP")
        else:
            LogStatus(_D(), "Disconnected ! ")