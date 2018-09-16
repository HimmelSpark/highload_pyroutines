import asyncio

from source.config.config import Config
from source.handler.handler import Handler


class Serevr(object):
    def __init__(self, config: Config, loop):
        self.config = config
        self.loop = loop

    async def launch_server(self):
        await asyncio.start_server(
            client_connected_cb=Handler(self.config.root_dir).handle(),
            host=self.config.host,
            port=self.config.port,
            loop=self.loop,
            reuse_port=True
        )