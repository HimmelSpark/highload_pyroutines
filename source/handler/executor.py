from config.config import Config
from handler.response import Response
import os
import aiofiles
import urllib.parse


class Executor(object):
    def __init__(self, config: Config):
        self.config = config

    async def execute(self, request: str) -> Response:
        #     return Response(Response.METHOD_NOT_ALLOWED)

        if len(request) == 0:
            return

        request = request.split('\r\n')

        line_1 = request[0].split(' ')
        method = line_1[0]

        path = line_1[1]
        path = urllib.parse.unquote(path)

        if path.find('?') > 1:
            path = path[0:path.find('?')]

        protocol = line_1[2]

        if method != 'HEAD' and method != 'GET':
            return Response(
                status=Response.METHOD_NOT_ALLOWED,
                protocol=protocol
            )

        full_path = self.config.root_dir + path

        if '../' in full_path:
            return Response(
                status=Response.NOT_FOUND,
                protocol=protocol
            )

        # print(full_path, os.getpid(), end='____________________\n')

        if os.path.isdir(full_path):
            if os.path.exists(full_path + 'index.html'):
                async with aiofiles.open(full_path + 'index.html', mode='rb') as file:
                    res = await file.read()
                    filesize = len(res)
                    if method == 'HEAD':
                        res = b''
                    file.close()

                    return Response(
                        status=Response.OK,
                        protocol=protocol,
                        content_type=Response.content_types['html'],
                        content_length=filesize,
                        body=res
                    )
            else:
                return Response(
                    status=Response.FORBIDDEN,
                    protocol=protocol
                )
        else:
            if os.path.exists(full_path):

                ftype = full_path.split('/')[-1].split('.')[-1]

                async with aiofiles.open(full_path, mode='rb') as file:
                    res = await file.read()
                    filesize = len(res)
                    if method == 'HEAD':
                        res = b''

                    file.close()

                    return Response(
                        status=Response.OK,
                        protocol=protocol,
                        content_type=Response.content_types.get(ftype, ''),  # контент тайп будет пустым
                        content_length=filesize,
                        body=res
                    )
            else:
                return Response(
                    status=Response.NOT_FOUND,
                    protocol=protocol
                )
