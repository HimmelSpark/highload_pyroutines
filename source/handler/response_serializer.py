from handler.response import Response


class ResponseSerializer(object):

    def __init__(self):
        pass

    @staticmethod
    def serialize(response: Response):

        # result =  '%s %s \r\n' \
        #          'Date:%s  \r\n' \
        #          'Content-Length:%s \r\n' \
        #          'Content-Type:%s \r\n' \
        #          'Server:%s \r\n' % (
        #     response.protocol,
        #     response.status,
        #     response.date,
        #     response.content_length,
        #     response.content_type,
        #     'server'
        # )
        #
        # return result.encode('ascii')

        #
        result = str()
        result += response.protocol
        result += ' ' + response.status + '\r\n'
        result += 'Date:{} \r\n'.format(response.date)
        result += 'Content-Length:{} \r\n'.format(response.content_length)
        result += 'Content-Type:{} \r\n'.format(response.content_type)
        result += 'Server:{}\r\n\r\n'.format('server')
        return result.encode('ascii')