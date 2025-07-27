default_config = {
    "GENERAL INFO":"Its general config.  Notise:\"candles minimal move percents\" is range of persents thets create minimal percent of cendl moowing calculated by increasing count of cendls",
    "Version of config": "2.0",
    "exchange": {
        "Bybit": {
            "API Public Key": "******************",
            "API Secret Key": "************************************",
            "Categoria of treyding": "linear",
            "SettleCoin": "USDT",
            "Testnet" : "False"
        },
        "Coins":[
                    "ATOMUSDT"
                ],
        "Trade":{
            "Max Tradeing Balance in USDT": 5,
            "First step in persent from treyding balance": 20,
            "Next steps prise in percent moowing from last order prise": 0.3,
            "Multiplier to increase the deal value": 0.5,
            "Sliding persent from entering prise":0.3,
            "Max count of candles for average a trade volume": 200,
            "Candle time": 1,

            "Take profit percent from entering prise": 0.5,
            "Stop lose percent from entering prise": 1.5,
            "leverage": 10,
            "Max Count of candle before forse closing order": 60,

            "Max orders per coin": 1,
            "Max position persent from balance": 5,

            "candles minimal move percents": [0.001, 0.1, 0.7, 3.5, 4],
            "Trigger turnover percent": 300,

            "time factor for trading turnover": "linear",

            "No Trade": "False",
            "Only Buy": "False",
            "Only Sell": "False",
            "All coins on exchange": "False"
    }
    },
    "Data base": {
        "Data base version": "1.0",
        "Data base name": "Log_Database",
        "Data base Logs table name": "logs",
        "data base host": "localhost",
        "Data base user": "fox",
        "Data base user_password": "********************************************************"
    }
}