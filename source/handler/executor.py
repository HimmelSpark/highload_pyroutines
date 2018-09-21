from handler.response import Response
import os
import aiofiles
import urllib.parse


class Executor:

    def __init__(self, root_dir: str()):
        self.root_dir = root_dir

    async def conc_is_dir(self, path: str) -> bool:
        return os.path.isdir(path)

    async def conc_file_exists(self, path: str) -> bool:
        return os.path.exists(path)


    async def execute(self, request: str) -> Response:

        if len(request) == 0:
            print('ERROR!!! GOT EMPTY REQUEST!!!')
            return Response(
                status=Response.FORBIDDEN,
                protocol='HTTP/1.1'
            )

        if 'HEAD' not in request and 'GET' not in request:
            return Response(
                status=Response.METHOD_NOT_ALLOWED,
                protocol='HTTP/1.1'
            )

        request = request.split('\r\n')

        method, path, protocol = request[0].split()

        path = urllib.parse.unquote(path)
        path = path.split('?')[0]

        if '../' in path:
            return Response(
                status=Response.NOT_FOUND,
                protocol=protocol
            )

        full_path = self.root_dir + path

        # if os.path.isdir(full_path):
        #     if os.path.exists(full_path + 'index.html'):
        #         async with aiofiles.open(full_path + 'index.html', mode='rb') as file:
        #             res = await file.read()
        #             filesize = len(res)
        #             if method == 'HEAD':
        #                 res = b''
        #             file.close()
        #
        #             return Response(
        #                 status=Response.OK,
        #                 protocol=protocol,
        #                 content_type=Response.content_types['html'],
        #                 content_length=filesize,
        #                 body=res
        #             )
        #     else:
        #         return Response(
        #             status=Response.FORBIDDEN,
        #             protocol=protocol
        #         )
        # else:
        #     if os.path.exists(full_path):
        #
        #         ftype = full_path.split('/')[-1].split('.')[-1]
        #
        #         async with aiofiles.open(full_path, mode='rb') as file:
        #             res = await file.read()
        #             filesize = len(res)
        #             if method == 'HEAD':
        #                 res = b''
        #
        #             file.close()
        #
        #             return Response(
        #                 status=Response.OK,
        #                 protocol=protocol,
        #                 content_type=Response.content_types.get(ftype, ''),  # контент тайп будет пустым
        #                 content_length=filesize,
        #                 body=res
        #             )
        #     else:
        #         return Response(
        #             status=Response.NOT_FOUND,
        #             protocol=protocol
        #         )

        if await self.conc_is_dir(full_path):
            if await self.conc_file_exists(full_path + 'index.html'):
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
            if await self.conc_file_exists(full_path):

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
