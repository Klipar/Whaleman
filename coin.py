from queueManager import QueueManager
from easy import Config
from bybit import Bybit

class Coin:
    def __init__(self, config: Config, coin: str, bybit: Bybit):
        from conditions import checkOrderConditions
        self.checkOrderConditions = checkOrderConditions

        self.bybit: Bybit = bybit
        self.config: Config = config

        self.coin: str = coin

    def roundQty (self, qty):
        return (round(float(qty) / self.qtyRounding) * self.qtyRounding)

    def roundPrise (self, prise):
        return round(float(prise), self.priseRounding)

    def setRounding(self, response):
        self.priseRounding = int(response['priceScale'])
        self.qtyRounding = float(response['lotSizeFilter']['qtyStep'])

    def processValues(self, data):
        data['data'].sort(key=lambda x: x["start"])

        for data in data['data']:
            self.pricesQueueManager.updateQueue(data)

        self.checkOrderConditions(self)

    def initialize (self, data):
        self.pricesQueueManager = QueueManager(data)

    def getLastPrise (self):
        return self.pricesQueueManager.getLatest().close
