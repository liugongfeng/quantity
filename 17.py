'''backtest
start: 2023-01-01 00:00:00
end: 2024-12-28 15:00:00
period: 1d
basePeriod: 1d
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"},{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

ChartCfg = {
    "__isStock": True,
    "title": {
        'text':'Python 画图'
    },

    'yAxis': [{
        'title': {'text': 'K Line'},
        'style': {'color': '#4572A7'},
        'opposite': True
    }, {
        'title': {'text': '指标轴'},
        'opposite': True
    } ],

    'series': [{
        'type': 'candlestick',
        'name': 'Current Time',
        'id': 'primary',
        'data': []
    }, {
        'type': 'line',
        'id': 'diff',
        'name':'DIF',
        'yAxis': 1,
        'data':[]
    }, {
        'type':'line',
        'id':'dea',
        'name':'DEA',
        'yAxis':1,
        'data':[]
    }, {
        'type':'line',
        'id':'macd',
        'name':'MACD',
        'yAxis':1,
        'data':[]
    } ]
}

def main():
    global ChartCfg
    preTime = 0
    chart = Chart(ChartCfg)
    chart.reset()
    while True:
        if exchange.IO("status"):
            exchange.SetContractType('rb888')
            while True:
                r = _C(exchange.GetRecords)
                if len(r) > 50:
                    break
            macd = TA.MACD(r)
            LogStatus(_D(), len(r))

            for i in range(len(r)):
                if r[i]["Time"] == preTime:
                    chart.add(0, [r[i]['Time'], r[i]['Open'], r[i]['High'], r[i]['Low'], r[i]['Close']], -1)
                    chart.add(1,[r[i]['Time'], macd[0][i]], -1)
                    chart.add(2,[r[i]['Time'], macd[1][i]], -1)
                    chart.add(3,[r[i]['Time'], macd[2][i]], -1)
                elif r[i]['Time'] > preTime:
                    chart.add(0, [r[i]['Time'], r[i]['Open'], r[i]['High'], r[i]['Low'], r[i]['Close']])
                    chart.add(1,[r[i]['Time'], macd[0][i]], -1)
                    chart.add(2,[r[i]['Time'], macd[1][i]], -1)
                    chart.add(3,[r[i]['Time'], macd[2][i]], -1)
                    preTime = r[i]['Time']
        else:
            LogStatus(_D(), "DisConnected!")
        Sleep(500)
                    
                    
