def main():
    exchange.SetContractType("MA888")
    # ticker = _C(exchange.GetTicker)
    # _CDelay(2000)
    # depth = _C(exchange.GetDepth)
    # Log(ticker)
    # Log(depth)
    record = _C(exchange.GetRecords, PERIOD_D1)
    Log(record)

    