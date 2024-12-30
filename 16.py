'''backtest
start: 2023-01-01 00:00:00
end: 2024-12-28 15:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"},{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

import json
def main():
    while True:
        if exchange.IO("status"):
            tab1 = {
                "type": "table",
                "title": "行情数据",
                "cols": ["项目", "数据"],
                "rows": []
            }
            tab2 = {
                "type": "table",
                "title": "账户数据",
                "cols": ["项目", "数据"],
                "rows": []
            }
            tab3 = {
                "type": "table",
                "title": "持仓数据",
                "cols": ["项目", "数据"],
                "rows": []
            }
            exchange.SetContractType("rb888")
            t = exchange.GetTicker()
            a = exchange.GetAccount()
            p = exchange.GetPosition()
            tab1['rows'].append(["Tick数据", json.dumps(t)])
            tab2['rows'].append(["账户数据", json.dumps(a)])
            tab3['rows'].append(["持仓数据", json.dumps(p)])
            
            LogStatus(_D(), "\n`" + json.dumps(tab1) + "`\n" + "`" + json.dumps(tab2) + "`\n" + "`" + json.dumps(tab3) + "`")
        else:
            LogStatus(_D(), "DisConnected!")
        Sleep(1000)



