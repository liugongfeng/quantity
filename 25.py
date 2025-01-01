'''backtest
start: 2023-01-01 00:00:00
end: 2024-12-28 15:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"},{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

def onTick():
    global preBarTime

    exchange.SetContractType("rb888")
    r = _C(exchange.GetRecords)
    if r[-1]["Time"] != preBarTime:
        preBarTime = r[-1]["Time"]
        Log("K line udpated! Do the trade Logic!")


def main():
    while True:
        if exchange.IO("status") :
            onTick()
            LogStatus(_D(), "Connected ! CTP")
        else:
            LogStatus(_D(), "DisConnected ! CTP")
            