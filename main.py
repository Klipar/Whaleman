from easy import Config
from coin import CoinHab
from bybit import Bybit
from easy.message import *

def main ():
    config = Config("Configs/developing.json")

    bybit = Bybit(config)

    coin_hab = CoinHab(config, bybit)
    coin_hab.Initialize_Coins(config, bybit)

    bybit.Subscribe(config, coin_hab)

    while True:
        bybit.Refresh_Positions()
        # config.refreshConfig()

if __name__ == "__main__":
    main()
