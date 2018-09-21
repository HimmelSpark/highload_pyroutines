from _datetime import datetime


class Response:
    OK = '200 OK'
    NOT_FOUND = '404 NOT FOUND'
    METHOD_NOT_ALLOWED = '405 NOT ALLOWED'
    FORBIDDEN = '403 FORBIDDEN'

    content_types = {
        'html': 'text/html',
        'css': 'text/css',
        'js': 'text/javascript',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'swf': 'application/x-shockwave-flash'
    }

    def __init__(self, status, protocol='', content_type='', content_length=0, body=b''):
        self.status = status
        self.protocol = protocol
        # self.connection = connection
        self.content_type = content_type
        self.content_length = content_length
        self.body = body
        self.date = datetime.today()

