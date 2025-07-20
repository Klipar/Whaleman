from config import Config
from coin import CoinHab
from bybit import Bybit
from telegram_info_bot import BOT_LAUNCHER, logTG
from easy.message import *
from multiprocessing import Process

def main ():
    conf = Config(Version = "2.0")          # Reading the configuration for exchange

    bybit = Bybit(conf)                     # Creating an exchange object.

    coin_hab = CoinHab(conf, bybit)
    coin_hab.Initialize_Coins(conf, bybit)

    bybit.Subscribe(conf, coin_hab)

    logTG(success("Bot started successfully!"))
    while 1:
        bybit.Refresh_Positions()
        conf.RefreshConfig(logTG)

def launcher():
    logTG(inform("Starting..."))
    Telebot_Process = Process(target=BOT_LAUNCHER)
    Telebot_Process.start()
    while (1):
        process = Process(target=main)
        process.start()
        process.join()
        logTG(failed("Bot stoped :("))
        logTG(inform("Restarting..."))

if __name__ == "__main__":
    launcher()
