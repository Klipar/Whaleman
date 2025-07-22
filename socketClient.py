import asyncio
from easy import Logger, Config

class SocketClient:
    def __init__(self, config: Config, logger=Logger()):
        self.config = config
        self.logger = logger

        self.reader: asyncio.StreamReader = None
        self.writer: asyncio.StreamWriter = None

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.config.getValue("Socket server", "host"), self.config.getValue("Socket server", "port"))
        print(f"Connection to {self.config.getValue("Socket server", "host")}:{self.config.getValue("Socket server", "port")}")

        asyncio.create_task(self.listen())

    async def send(self, message: str) -> None:
        if self.writer is None:
            print("No connection.")
            return
        self.writer.write((message + '\n').encode('utf-8'))
        await self.writer.drain()

    async def listen(self):
        try:
            while True:
                data = await self.reader.readline()
                if not data:
                    print("The server has closed the connection")
                    break
                print(f"{data.decode().strip()}")
        except Exception as e:
            print(f"Reading error: {e}")
        finally:
            self.writer.close()
            await self.writer.wait_closed()
