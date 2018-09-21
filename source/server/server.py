import asyncio
import socket

from config.config import Config
from handler.handler import Handler


class Server(object):
    def __init__(self, config: Config, loop, handler: Handler, sock: socket):
        self.config = config
        self.loop = loop
        self.handler = handler
        self.sock = sock

    async def launch_server(self):
        await asyncio.start_server(
            client_connected_cb=self.handler.handle,
            sock=self.sock,
            loop=self.loop,
            reuse_port=True
        )