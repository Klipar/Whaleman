from config import Config
from coin import CoinHab # Coin, Coin_Set
from bybit import Bybit
from telegram_info_bot import *
import asyncio
from easy.massage import failed, success, inform, warn, test
from time import sleep
from telegram_info_bot import TG_LOG
from multiprocessing import Process

def main ():
    conf = Config(Version = "2.0")         # читаємо конфіг
    # bot = TeleGramLogBot(autostart = True)  #
    
    bybit = Bybit(conf)     # cтворюємо об'єкт біржі

    coin_hab = CoinHab(conf, bybit)

    coin_hab.Initialize_Coins(conf, bybit)

    bybit.Subscribe(conf, coin_hab)

    TG_LOG(success("Bot started successfully!"))
    while 1:
        bybit.Refresh_Positions()
        conf.Refresh(TG_LOG)
def launcher():
    TG_LOG(inform("Starting..."))
    Telebot_Process = Process(target=BOT_LAUNCHER)
    Telebot_Process.start()
    while (1):
        process = Process(target=main)
        process.start()
        process.join()
        TG_LOG(failed("Bot stoped :("))
        TG_LOG(inform("Restarting..."))



if __name__ == "__main__":
    launcher()
