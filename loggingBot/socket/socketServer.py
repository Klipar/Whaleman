import asyncio
import json
from easy import Logger, Config
from typing import Callable, Dict, Any

class SocketServer:
    def __init__(self, config: Config,
                 actionsHolder: Dict[str, Callable],
                 logger=Logger()):
        self.config = config
        self.logger = logger
        self.actionsHolder = actionsHolder

        self.clients: set[asyncio.StreamWriter] = set()

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self.clients.add(writer)
        addr = writer.get_extra_info('peername')
        self.logger.inform(f"Connection to {addr}")
        try:
            while True:
                data = await reader.readline()
                if not data: break

                message = json.loads(data.decode('utf-8'))

                await self.actionsHolder[message["action"]](message["data"])

                writer.write("Ok.\n".encode('utf-8'))
                await writer.drain()
        except Exception as e:
            self.logger.failed(f"Error in client: {e}")
        finally:
            self.clients.discard(writer)
            writer.close()
            await writer.wait_closed()
            self.logger.inform(f"Connection closed: {addr}")

    async def broadcast(self, data: Dict[str, Any]):
        for writer in list(self.clients):
            try:
                writer.write(json.dumps(data).encode('utf-8') + b'\n')
                await writer.drain()
            except Exception:
                self.clients.discard(writer)

    async def start(self):
        server = await asyncio.start_server(self.handle_client, self.config.getValue('Socket server', 'host'), self.config.getValue('Socket server', 'port'))
        self.logger.inform(f"Socket server is running on {self.config.getValue('Socket server', 'host')}:{self.config.getValue('Socket server', 'port')}")
        async with server:
            await server.serve_forever()
