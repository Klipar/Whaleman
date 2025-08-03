import asyncio
import json
from typing import Any, Callable, Dict
from easy import Logger, Config

class SocketClient:
    def __init__(self, config: Config, actionsHolder: Dict[str, Callable], logger=Logger()):
        self.config = config
        self.logger = logger
        self.actionsHolder = actionsHolder

        self.reader: asyncio.StreamReader = None
        self.writer: asyncio.StreamWriter = None

    def isConnect(self) -> bool:
        return self.reader is not None and self.writer is not None

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
                message = await self.reader.readline()
                if message:
                    try:
                        message = message.decode('utf-8').strip()
                        if message == 'Ok.':
                            continue

                        action = json.loads(message)
                        await self.actionsHolder[action["action"]](action["data"])
                    except Exception as e:
                        self.logger.failed(f"error in socket client:\n{e}")
                else:
                    self.logger.inform("The server has closed the connection")
                    break

        except Exception as e:
            self.logger.failed(f"Reading error: {e}")
        finally:
            await self.disconnect()

    async def disconnect(self) -> None:
        if (self.writer):
            try:
                self.writer.close()
                await self.writer.wait_closed()
                self.reader = self.writer = None
                self.logger.success("Connection successfully closed!")

            except Exception as e:
                self.logger.failed(f"Failed to close socket connection:\n{e}")
