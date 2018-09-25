import logging
from asyncio import StreamReader, StreamWriter

from handler.executor import Executor
from handler.response_serializer import ResponseSerializer


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


        if len(data) > 0:

            request = data.decode('utf-8').strip('\r\n')

            response, fileGenerator = await self.executor.execute(request)

            data = ResponseSerializer.serialize(response=response)
            writer.write(data)
            await writer.drain()

            if fileGenerator != None:
                while True:
                    try:
                        chunk = next(fileGenerator)
                        writer.write(chunk)
                        await writer.drain()
                        if not chunk:
                            raise StopIteration
                    except ConnectionResetError:
                        logging.info('ConnectionResetError')
                        writer.close()
                        break
                    except StopIteration:
                        writer.close()
                        break

        writer.close()
