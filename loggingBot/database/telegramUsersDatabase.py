from typing import List
import sqlite3
from easy import Config, Logger

class TelegramUsersDatabase:
    def __init__(self, config: Config, logger: Logger = Logger()):
        self.config = config
        self.logger = logger

        self.logger.inform("Connecting to users database")
        self.conn = sqlite3.connect(config.getValue("Users database"))
        self.cursor = self.conn.cursor()

        self.createDatabaseIfIdDasNotExist()
        self.logger.success("Connection executed successfully!")

    def createDatabaseIfIdDasNotExist(self) -> None:
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            TelegramID INTEGER PRIMARY KEY,
            subscribed INTEGER NOT NULL,
            sudo INTEGER NOT NULL
        )
        ''')

        self.conn.commit()

    def __del__(self):
        self.conn.close()
        self.logger.inform("Connection to database closed.")

    def getTelegramIDForAllSubscribedUsers(self) -> List[int]:
        self.cursor.execute('SELECT TelegramID FROM users WHERE subscribed=1')
        rows = self.cursor.fetchall()
        return [item[0] for item in rows]

    def getTelegramIDForAllSubscribedAdmins(self) -> List[int]:
        self.cursor.execute('SELECT TelegramID FROM users WHERE sudo=1 and subscribed=1')
        rows = self.cursor.fetchall()
        return [item[0] for item in rows]

    def getUser(self, TelegramID: int):
        self.cursor.execute('SELECT * FROM users WHERE TelegramID=?', (TelegramID,))
        rows = self.cursor.fetchall()
        return [item for item in rows[0]] if rows else None

    def addOrUpdateUser(self, TelegramID: int, subscribed: int = 0, sudo: int = 0):
        self.cursor.execute('''
        INSERT OR REPLACE INTO users (TelegramID, subscribed, sudo) VALUES (?, ?, ?)
        ''', (TelegramID, subscribed, sudo))
        self.conn.commit()
