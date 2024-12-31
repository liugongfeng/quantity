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
            exchange.SetContractType("MA888")
            r = _C(exchange.GetRecords)
            R = _C(exchange.GetRecords)
            if len(r) < 10:
                continue
            ma1 = TA.MA(R, 5)
            ma2 = TA.MA(R, 10)
            ext.PlotRecords(r, "MA888")
            ext.PlotLine("ma1", ma1[-2], r[-2]["Time"])
            ext.PlotLine("ma2", ma1[-2], r[-2]["Time"])
            ret = _Cross(ma1, ma2)
            LogStatus(_D(), "Connected!", "ret: ", ret)
        else:
            LogStatus(_D(), "disConnected!")
        Sleep(1000)
            
            

    