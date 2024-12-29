'''backtest
start: 2023-01-01 00:00:00
end: 2024-12-28 15:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"},{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

def main():
    while not exchange.IO("status"):
        LogStatus("Connecting...." + _D())
    
    Log("ALL Contract")
    instruments = _C(exchange.IO, "instruments")
    Log("Contracts Done ! ")
    lenghth = 0
    for i in range(len(instruments)):
        lenghth += 1
    Log("The length of Contracts: ", lenghth)
