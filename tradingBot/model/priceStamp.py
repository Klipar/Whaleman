from typing import Any, Dict

class PriceStamp:
    def __init__(self, data: Dict[str, Any]):
        self.__setVariableData(data)
        self.__setStaticData(data)

    def updateStamp(self, data: Dict[str, Any]) -> bool:
        """Returns True if the data has been successfully updated. If the data already belongs to another candle, it will return False."""
        if int(data["start"]) == self.start:
            self.__setVariableData(data)
            return True

        return False

    def __setVariableData(self, data: Dict[str, Any]) -> None:
        self.timestamp = int(data["timestamp"])
        self.open = float(data["open"])
        self.high = float(data["high"])
        self.low = float(data["low"])
        self.close = float(data["close"])
        self.volume = float(data["volume"])
        self.turnover = float(data["turnover"])
        self.confirm = data["confirm"]

    def __setStaticData(self, data: Dict[str, Any]) -> None:
        self.start = int(data["start"])
        self.end = int(data["end"])
        self.interval = int(data["interval"])
