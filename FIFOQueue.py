from collections import deque
from typing import Any, List

class FIFOQueue:
    """A class that implements queue functionality for storing data from the exchange."""
    def __init__(self, queue: deque = None):
        self.queue = queue if queue else deque()

    def enqueueAndDequeue(self, item: Any) -> None:
        """Add a new item to the queue and remove the oldest one if needed."""
        self.queue.append(item)
        if len(self.queue) > 1:
            self.queue.popleft()

    def enqueueList(self, items: List[Any]) -> None:
        """Add a list of items to the queue."""
        self.queue.extend(items)

    def view(self) -> List[Any]:
        """View all items in the queue."""
        return list(self.queue)

    def isEmpty(self) -> bool:
        """Check if the queue is empty."""
        return len(self.queue) == 0

    def size(self) -> int:
        """Get the number of items in the queue."""
        return len(self.queue)

    def latest(self) -> Any:
            """Get the most recently added item in the queue."""
            if self.isEmpty():
                return None
            return self.queue[-1]

    def secondLatest(self) -> Any:
        """Get the second most recently added item in the queue."""
        if len(self.queue) < 2:
            return None
        return self.queue[-2]

    def replaceQueue(self, items: List[Any]) -> None:
        """Replace the entire queue with a new list of items."""
        self.queue = deque(items)
