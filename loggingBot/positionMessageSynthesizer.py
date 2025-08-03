import json
from string import Template
from typing import Any, Dict

from easy import Config, Logger

class LoggingMessageSynthesizer:
    def __init__(self, config: Config, logger: Logger = Logger()):
        self.config = config
        self.logger = logger

    def getSynthesizerOrderMessage(self, data: Dict[str, Any]) -> str:
        Value = round(data["qty"]*data["prise"], 2)
        profit = round(abs(data["takeProfit"]*data["qty"]-data["prise"]*data["qty"])*data["leverage"], 2)
        loss  = round(abs(data["stopLoss"]*data["qty"]-data["prise"]*data["qty"])*-1*data["leverage"], 2)

        template = Template(self.config.getValue("Events", data["side"]))
        synthesizedString = template.substitute(symbol=data["symbol"],
                                               prise=data["prise"],
                                               takeProfit=data["takeProfit"],
                                               stopLoss=data["stopLoss"],
                                               qty=data["qty"],
                                               Value=Value,
                                               profit=profit,
                                               loss=loss)

        return synthesizedString

    def getSynthesizerOrderListMessage(self, data: Dict[str, Any]) -> str:
        if data["ordersData"] == []:
            return self.config.getValue("Events", "NoOpenedOrders")

        template = Template(self.config.getValue("Events", "openedOrders"))
        return template.substitute(ordersData=json.dumps(data["ordersData"], indent=4))
