from source.handler.response import Response


class ResponseSerializer(object):

    def __init__(self):
        pass

    @staticmethod
    def serialize(response: Response):
        result = str()
        result += response.protocol
        result += ' ' + response.status + '\n'
        result += 'Date: {} \n'.format(response.date)
        result += 'Content-Length: {} \n'.format(response.content_length)
        result += 'Content-Type: {} \n'.format(response.content_type)
        result += 'Connection: {}\n'.format(response.connection)
        result += 'Server: {}\r\n\r\n'.format('server')
        return result.encode('ascii') + response.body