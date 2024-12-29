'''backtest
start: 2023-01-01 00:00:00
end: 2024-12-28 15:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"},{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

def main():
    ctList = ["rb888", "i888", "MA888", "pp888"]
    while True:        
        if exchange.IO("status"):
            for i in range(len(ctList)):
                ret = exchange.SetContractType(ctList[i])
                t = exchange.GetTicker()
                exchange.SetDirection("sell")
                exchange.Sell(t.Buy - 10, 1, "HeYue: ", ctList[i], "->", ret["InstrumentID"])
                orders = exchange.GetOrders()
                Log("orders length: ", len(orders), "orders:", orders)
                pos = exchange.GetPosition()
                for i in range(len(pos)):
                    Log(pos[i])
                break
        else:
            LogStatus(_D(), "DisConnected! CTP")
    
