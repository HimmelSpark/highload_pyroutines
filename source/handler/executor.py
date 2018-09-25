from handler.response import Response
from handler.asyncFileReader import async_get

import aiofiles
import urllib.parse
import logging
import os



class Executor:
    def __init__(self, root_dir: str()):
        self.root_dir = root_dir


    async def readFile(self, path: str) -> bytes:
        async with aiofiles.open(path, 'rb') as f:
            return await f.read()

    async def readFileByChunk(self, path: str) -> bytes:
        with open(path, 'rb') as f:
            while True:
                chunk = f.read(1)
                if not chunk:
                    break
                yield chunk

    async def execute(self, request: str) -> []:

        if len(request) == 0:
            print('ERROR!!! GOT EMPTY REQUEST!!!')
            return Response(
                status=Response.FORBIDDEN,
                protocol='HTTP/1.1'
            ), None

        if 'HEAD' not in request and 'GET' not in request:
            return Response(
                status=Response.METHOD_NOT_ALLOWED,
                protocol='HTTP/1.1'
            ), None

        request = request.split('\r\n')

        method, path, protocol = request[0].split()

        path = urllib.parse.unquote(path)
        path = path.split('?')[0]

        if '../' in path:
            return Response(
                status=Response.NOT_FOUND,
                protocol=protocol
            ), None

        full_path = self.root_dir + path

        if '.' in full_path.split('/')[-1]:  # if filename provided

            try:
                ftype = full_path.split('/')[-1].split('.')[-1]
                fileGenerator = None
                if method == 'GET':
                    fileGenerator = async_get(full_path)
                filesize = os.path.getsize(full_path)

                return Response(
                    status=Response.OK,
                    protocol=protocol,
                    content_type=Response.content_types.get(ftype, ''),
                    content_length=filesize
                ), fileGenerator

            except FileNotFoundError:  # file not found

                logging.info('file: {} not found'.format(full_path))

                return Response(
                    status=Response.NOT_FOUND,
                    protocol=protocol
                ), None

        else:  # if dirname provided

            try:

                filesize = os.path.getsize(full_path + 'index.html')

                fileGenerator = async_get(full_path + 'index.html')

                return Response(
                    status=Response.OK,
                    protocol=protocol,
                    content_type=Response.content_types['html'],
                    content_length=filesize
                ), fileGenerator

            except FileNotFoundError:  # .html file not found

                logging.info('No .html file in {} directory'.format(full_path))

                return Response(
                    status=Response.FORBIDDEN,
                    protocol=protocol
                ), None
