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
            LogStatus(_D(), "Connected!")
            cmd = GetCommand()
            if cmd:
                Log(cmd)
        else:
            LogStatus(_D(), "DisConnected!")
        Sleep(1000)
