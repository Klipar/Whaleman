from easy import Config, Logger
from socketClient import SocketClient

class TelegramLogger:
    def __init__(self, config: Config, logger: Logger = None):
        self.logger: Logger = logger if logger else Logger()
        self.config: Config = config

        self.socketClient: SocketClient = SocketClient(config)

    async def connect(self) -> None:
        await self.socketClient.connect()

    async def sendToAll(self, message: str) -> None:
        templates = self.config.getValue("Socket server", "Massages", "Send to all")
        templates["data"]["message"] = message
        await self.socketClient.send(templates)

    async def sendToAdmins(self, message: str) -> None:
        templates = self.config.getValue("Socket server", "Massages", "Send to admins")
        templates["data"]["message"] = message
        await self.socketClient.send(templates)

    async def sendPlacingOrder(self, side, prise, takeProfit, stopLoss, symbol, qty, leverage) -> None:
        templates = self.config.getValue("Socket server", "Massages", "Place order")
        templates["data"] = {"side": side,
                            "prise" : prise,
                            "takeProfit" : takeProfit,
                            "stopLoss" : stopLoss,
                            "symbol" : symbol,
                            "qty" : qty,
                            "leverage" : leverage}
        await self.socketClient.send(templates)
