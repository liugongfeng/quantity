'''backtest
start: 2023-01-01 00:00:00
end: 2024-12-28 15:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"},{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

def main():
    tradeCount = _G("addCount")
    if tradeCount:
        Log("恢复加仓次数 数据：", tradeCount)
    else:
        tradeCount = 0
        Log("初始运行，加仓次数：", tradeCount)
    
    while True:
        if exchange.IO("status"):
            exchange.SetContractType("MA888")
            exchange.GetTicker()
            LogStatus(_D(), "Connected! ", "IsVirtual(): ", IsVirtual())
            cmd = GetCommand()
            if cmd:
                tradeCount += 1
                Log("加仓次数: ", tradeCount)
                Log("保存加仓次数: ", tradeCount)
                _G("addCount", tradeCount)
        
        else:
            LogStatus(_D(), "DisConnected! ", "IsVirtual(): ", IsVirtual())
        Sleep(1000)