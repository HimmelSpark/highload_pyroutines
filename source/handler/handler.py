from asyncio import StreamReader, StreamWriter

from handler.executor import Executor
from handler.response_serializer import ResponseSerializer
from handler.response import Response


import logging

class Handler(object):
    def __init__(self, root, executor: Executor):
        self.root = root
        self.executor = executor

    async def handle(self, reader: StreamReader, writer: StreamWriter) -> None:

        data = b''

        while True:

            data += await reader.read(1024)

            if not data or reader.at_eof():
                writer.write(ResponseSerializer.serialize(Response(status=Response.METHOD_NOT_ALLOWED))) #TODO: такого быть не должно!!!
                return

            if data[-4:] == b'\r\n\r\n':
                break

        if data == b'':
            writer.write(ResponseSerializer.serialize(Response(status=Response.METHOD_NOT_ALLOWED))) #TODO: и этого тоже
            print('shit happened')
            await writer.drain()
            return


        if len(data) > 0:
            request = data.decode('utf-8').strip('\r\n')
            response = await self.executor.execute(request)
            data = ResponseSerializer.serialize(response=response)
            writer.write(data)
            await writer.drain()
        writer.close()
