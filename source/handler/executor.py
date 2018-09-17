from source.config.config import Config
from source.handler.response import Response
import os
import aiofiles


class Executor(object):
    def __init__(self, config: Config):
        self.config = config

    async def execute(self, request: str) -> Response:
        #     return Response(Response.METHOD_NOT_ALLOWED)
        request = request.split('\r\n')

        line_1 = request[0].split(' ')
        method = line_1[0]
        path = line_1[1]
        protocol = line_1[2]

        line_2 = request[1].split(' ')
        host = line_2[1]

        line_3 = request[2].split(' ')
        connection = line_3[1]

        if method != 'HEAD' and method != 'GET':
            return Response(
                status=Response.METHOD_NOT_ALLOWED,
                protocol=protocol,
                connection=connection,
            )

        full_path = self.config.root_dir + path

        if '../' in full_path:
            return Response(
                status=Response.NOT_FOUND,
                protocol=protocol,
                connection=connection
            )

        if os.path.isdir(full_path):
            if os.path.exists(full_path + 'index.html'):
                async with aiofiles.open(full_path + 'index.html', mode='rb') as file:
                    res = await file.read()
                    return Response(
                        status=Response.OK,
                        protocol=protocol,
                        connection=connection,
                        content_type=Response.content_types['html'],
                        content_length=len(res),
                        body=res
                    )
            else:
                return Response(
                    status=Response.NOT_FOUND,
                    protocol=protocol,
                    connection=connection
                )
        else:
            if os.path.exists(full_path):
                ftype = full_path.split('/')[-1].split('.')[-1]
                async with aiofiles.open(full_path, mode='rb') as file:
                    res = await file.read()
                    return Response(
                        status=Response.OK,
                        protocol=protocol,
                        connection=connection,
                        content_type=Response.content_types.get(ftype, ''),  # контент тайп будет пустым
                        content_length=len(res),
                        body=res
                    )
            else:
                return Response(
                    status=Response.NOT_FOUND,
                    protocol=protocol,
                    connection=connection
                )
