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
            exchange.SetContractType('MA888')
            exchange.GetTicker()

            LogStatus(_D(), "Connected!", "IsVirtual(): ", IsVirtual())
        else:
            LogStatus(_D(), "DisConnected!", "IsVirtual(): ", IsVirtual())
        Sleep(1000)