from easy import Logger
from typing import Dict, List, Union
from FIFOQueue import FIFOQueue
from priceStamp import PriceStamp

class QueueManager:
    def __init__(self, data: Dict[str, Union[str, int]]):
        self.initQueue(data)

    def initQueue(self, data) -> None:
        self.queue = FIFOQueue()

        candleTime: int = int(data["result"]["list"][0][0])-int(data["result"]["list"][1][0])

        priceStumpList: List[PriceStamp] = []

        for candle in reversed(data["result"]["list"]):
            end: int = int(candle[0])+candleTime-1

            priceStumpList.append(PriceStamp({"start": candle[0],
                                              "end": end,
                                              "interval": candleTime/60000,
                                              "open": candle[1],
                                              "high": candle[2],
                                              "low": candle[3],
                                              "close": candle[4],
                                              "volume": candle[5],
                                              "turnover": candle[6],
                                              "confirm": True,
                                              "timestamp": end}))

        priceStumpList[-1].timestamp = data["time"]
        priceStumpList[-1].confirm = False

        self.queue.replaceQueue(priceStumpList)

    def updateQueue(self, data) -> None:
        lastPriceStamp: PriceStamp = self.queue.latest()
        if lastPriceStamp.updateStamp(data): # Just update on current candle
            return

        elif int(data['start']) > lastPriceStamp.start: # Check if the data is not corrupted (if no candles are missing)
            secondLastPriceStamp: PriceStamp = self.queue.secondLatest()
            timeDelta = lastPriceStamp.start - secondLastPriceStamp.start
            if lastPriceStamp.start+timeDelta == int(data['start']): # Data is correct. Just adding new candle
                self.queue.enqueueAndDequeue(PriceStamp(data))

            else: # data is not correct, one or mode candle lost. Required restructuring
                pass # TODO: write call back for fool updating candle data (coinHab.Initialize_Coins())

        else: # we get update on old candle. searching and updating
            queueList: List[PriceStamp] = self.queue.view()
            for stamp in queueList:
                if int(data['start']) == stamp.start:
                    stamp.updateStamp(data)

            self.queue.replaceQueue(queueList)
