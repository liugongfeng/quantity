'''backtest
start: 2023-01-01 00:00:00
end: 2024-12-18 15:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"},{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

def main():
    contractTypeList = ["MA888", "rb888", "i888"]
    while True:
        if exchange.IO("status"):
            for i in range(len(contractTypeList)):
                ret = exchange.SetContractType(contractTypeList[i])
                ticker = exchange.GetTicker()
                exchange.SetDirection("sell")
                id = exchange.Sell(ticker.Sell, 1)
                Log(contractTypeList[i], "Order ID: ", id)
            orders = exchange.GetOrders()
            for i in range(len(orders)):
                Log(orders[i])
            break
        else:
            LogStatus(_D(), "DisConnected!")