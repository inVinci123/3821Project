import yfinance

stuffs = [
    "AAPL", "MSFT", "AMZN", "NVDA", "BTC-USD",
    "CBA.AX", "BHP.AX", "NEM.AX", "NAB.AX", "WBC.AX", "ANZ.AX", "CSL.AX",
    "WES.AX", "MQG.AX", "XYZ.AX", "GMG.AX", "RMD.AX", "FMG.AX", "TLS.AX",
    "RIO.AX", "TCL.AX", "WDS.AX", "ALL.AX", "NST.AX", "SIG.AX", "BXB.AX",
    "QBE.AX", "WOW.AX", "PME.AX", "COL.AX", "REA.AX", "WTC.AX", "AMC.AX",
    "NWS.AX", "XRO.AX", "ENV.AX", "VAS.AX", "SUN.AX", "STO.AX", "SCG.AX",
    "COH.AX", "QAN.AX"
]

for stock in stuffs:
    ticker = yfinance.Ticker(stock)
    historical_data = ticker.history(period="1y")
    data = historical_data.to_csv(date_format="%d/%m/%Y")

    # imagine having the data in DataFrame form, then just doing
    # text processing on its CSV output.
    output = []
    for line in data.strip().split('\n'):
        line = line.strip()
        if line.startswith("Date"):
            output.append("Date,Value")
            continue
        components = line.split(',')
        key_points = (float(x) for x in components[1:5])
        output.append(components[0] + ',' + str(sum(key_points) / 4))

    fileout = stock.lower() + ".csv"
    with open(fileout, "w") as OUTPUT:
        OUTPUT.write('\n'.join(output))

