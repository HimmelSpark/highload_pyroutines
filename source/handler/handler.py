from asyncio import StreamReader, StreamWriter

from source.handler.executor import Executor
from source.handler.response_serializer import ResponseSerializer


class Handler(object):
    def __init__(self, root, executor: Executor):
        self.root = root
        self.executor = executor

    async def handle(self, reader: StreamReader, writer: StreamWriter) -> None:

        data = b''

        while True:
            data += await reader.read(1024)

            if not data or reader.at_eof():
                break

            if data[-4:] == b'\r\n\r\n':
                break

        request = self.decode_data(data)
        response = await self.executor.execute(request)
        data = ResponseSerializer.serialize(response=response)
        print(data)
        writer.write(data)
        await writer.drain()
        writer.close()

    def decode_data(self, data: bytearray):
        return data.decode('utf-8').strip('\r\n')