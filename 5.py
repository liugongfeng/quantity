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
            ret = exchange.SetContractType("MA888")
            Log("Info: ", ret)
            break
        else:
            LogStatus(_D(), "DisConnected!")