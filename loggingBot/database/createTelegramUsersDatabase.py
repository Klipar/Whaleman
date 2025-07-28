from easy import Config
import sqlite3

config = Config(configPath="Configs/telegramBot.json",
                onFailedToLoadConfig=lambda: exit(0))

conn = sqlite3.connect(config.getValue("Users database"))
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    TelegramID INTEGER PRIMARY KEY,
    subscribed INTEGER NOT NULL,
    sudo INTEGER NOT NULL
)
''')

conn.commit()
conn.close()
