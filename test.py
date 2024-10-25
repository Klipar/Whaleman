from pybit.unified_trading import HTTP
session = HTTP(
    testnet=False,
    api_key="IIRzKTkms06kYY0Wug",
    api_secret="wJEPNA7Gtoz7QO9ETOXYShw7RC3aVJ1zFeKT",
)

CountOfCandleBeforeMarketStop = 5
CendelTime = 1
Sliding_Persend = 0.005
TreydCategory = "linear"

result = (session.get_positions(
    category="linear",
    settleCoin="USDT",
))





for i in result['result']['list']:
    if (int(result['time']) >= int(i['updatedTime'])+1000*CendelTime*CountOfCandleBeforeMarketStop):
        print (i['updatedTime'])

        t = (session.get_kline(
            category="linear",
            symbol=i['symbol'],
            interval=1,
            limit=1
        ))
        tp = float(t['result']['list'][0][4])
        sl = float(t['result']['list'][0][4])-5
        print(session.set_trading_stop(
            category="linear",
            symbol=i['symbol'],
            stopLoss=tp,
            slTriggerBy="MarkPrice",
            positionIdx=0
        ))