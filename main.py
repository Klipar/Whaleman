from config import Config
from coin import CoinHab
from bybit import Bybit
from telegram_info_bot import BOT_LAUNCHER, TG_LOG
from easy.message import *
from multiprocessing import Process

def main ():
    conf = Config(Version = "2.0")          # Reading the configuration for exchange

    bybit = Bybit(conf)                     # Creating an exchange object.

    coin_hab = CoinHab(conf, bybit)
    coin_hab.Initialize_Coins(conf, bybit)

    bybit.Subscribe(conf, coin_hab)

    TG_LOG(success("Bot started successfully!"))
    while 1:
        bybit.Refresh_Positions()
        conf.RefreshConfig(TG_LOG)

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
