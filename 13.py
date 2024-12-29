'''backtest
start: 2023-01-01 00:00:00
end: 2024-12-28 15:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"},{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

def main():
    while True:
        if exchange.IO("status"):
            exchange.SetContractType("rb888")
            account = exchange.GetAccount()
            Log("Gua Dan Qian:")
            Log("Account , Balance", account["Balance"])
            ticker = exchange.GetTicker()
            exchange.SetDirection("buy")
            exchange.Buy(ticker.Buy - 10, 1)
            account = exchange.GetAccount()
            Log("Gua Dan Hou:")
            Log("Account , Balance", account["Balance"])
            Log("Frozen Balance: ", account["FrozenBalance"])
            LogStatus(_D(), "Connected! CTP")
            break
        else:
            LogStatus(_D(), "DisConnected! CTP")
    
