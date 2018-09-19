from handler.response import Response


class ResponseSerializer(object):

    def __init__(self):
        pass

    @staticmethod
    def serialize(response: Response):
        result = str()
        result += response.protocol
        result += ' ' + response.status + '\r\n'
        result += 'Date:{} \r\n'.format(response.date)
        result += 'Content-Length:{} \r\n'.format(response.content_length)
        result += 'Content-Type:{} \r\n'.format(response.content_type)
        # result += 'Connection: {}\n'.format(response.connection)
        result += 'Server:{}\r\n\r\n'.format('server')
        return result.encode('ascii') + response.body