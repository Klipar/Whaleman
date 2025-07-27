from FIFOQueue import FIFOQueue
from priceStamp import PriceStamp

class QueueManager:
    def __init__(self):
        self.queue = FIFOQueue()

    def initQueue(self, data) -> None:
        if self.queue.isEmpty():
            pass
        else:
            pass
