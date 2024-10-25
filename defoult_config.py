default_config = {
    "GENERAL INFO":"Its general config.  Notise:\"cendel minimal move persents\" is range of persents thets create minimal percent of cendl moowing calculated by increasing count of cendls",
    "Version of config": "2.0",
    "exchange": {
        "Bybit": {
            "API Pyblic Key": "IIRzKTkms06kYY0Wug",
            "API Secret Key": "wJEPNA7Gtoz7QO9ETOXYShw7RC3aVJ1zFeKT",
            "Categoria of treyding": "linear",
            "SettleCoin":     "USDT"
        },
        "Coins":[
                    "ATOMUSDT"
                ],
        "Treyd":{
            "Max Treyding Balance in USDT": 5,
            "First step in persent from treyding balance": 20,
            "Next steps prise in percent moowing from last order prise": 0.3, 
            "Multiplier to increase the deal value": 0.5,
            "Sliding persent from entering prise":0.3,
            "Max count of cendals for awereg a treyd wolume": 200,
            "Cendel time": 1,

            "Take profit percent from entering prise": 0.5,
            "Stop lose percent from entering prise": 1.5,
            "leverage": 10,

            "Max orders per coin": 1,
            "Max position persent from balance": 5,
            
            "cendel minimal move persents": [0.001, 0.1, 0.7, 3.5, 4],
            "Triger turnover persent": 300,

            "time factor for trading turnover": "linear",
            
            "No Treyd": "False",
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
        "Data base user_password": "SJQO1HG08xwPU43E4#@&5Y*^Nyc0f7PWAO3eOypLw1G7Hjt6UaTFqE3d"
    }
}