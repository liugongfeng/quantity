'''backtest
start: 2023-01-01 00:00:00
end: 2024-12-28 15:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"},{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

import matplotlib.pyplot as plt

def main():
    Log("Hello world! @")
    Sleep(1000 * 5)
    Log("Hello world!, #ff0000@")

    Log("`Data: image/png;base64,AAAA`")

    plt.plot([3,6,2,4,7,11])
    Log(plt)
