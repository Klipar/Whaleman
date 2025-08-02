import asyncio
import json
from typing import Any, Dict
from easy import Logger, Config

class SocketClient:
    def __init__(self, config: Config, logger=Logger()):
        self.config = config
        self.logger = logger

        self.reader: asyncio.StreamReader = None
        self.writer: asyncio.StreamWriter = None

    async def connect(self) -> None:
        self.reader, self.writer = await asyncio.open_connection(self.config.getValue("Socket server", "host"), self.config.getValue("Socket server", "port"))
        self.logger.inform(f"Connection to {self.config.getValue('Socket server', 'host')}:{self.config.getValue('Socket server', 'port')}")

        asyncio.create_task(self.listen())

    async def send(self, data: Dict[str, Any]) -> None:
        if self.writer is None:
            self.logger.failed("No connection.")
            return
        self.writer.write((json.dumps(data) + '\n').encode('utf-8'))
        await self.writer.drain()

    async def listen(self) -> None:
        try:
            while True:
                data = await self.reader.readline()
                if not data:
                    self.logger.inform("The server has closed the connection")
                    break

        except Exception as e:
            self.logger.failed(f"Reading error: {e}")
        finally:
            self.writer.close()
            await self.writer.wait_closed()

    async def disconnect(self) -> None:
        if (self.writer):
            try:
                self.writer.close()
                await self.writer.wait_closed()
            except Exception as e:
                self.logger.failed(f"Failed to close socket connection:\n{e}")
