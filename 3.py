'''backtest
start: 2023-01-01 00:00:00
end: 2024-12-18 15:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"},{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

def main():
    exchange.SetContractType("MA888")
    Log(exchange.GetRecords(60*2))
    Log(exchange.GetRecords(PERIOD_M5))
    