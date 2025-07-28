from loggingBot.database.telegramUsersDatabase import TelegramUsersDatabase
from loggingBot.telegramInfoBot import TeleGramLogBot
from easy import Config, Logger

def startTelegramBot():
    config = Config(configPath="Configs/telegramBot.json",
                    logger=Logger(2),
                    onFailedToLoadConfig=lambda: exit(0))

    bot = TeleGramLogBot(config = config,
                         database =TelegramUsersDatabase(config),
                         logger=Logger())

    bot.run()

if __name__ == "__main__":
    startTelegramBot()
