class Request(object):
    def __init__(self, data: str):
        if 'GET' not in data or 'HEAD' not in data:
            pass
        # self.method
        # self.protocol
        # self.url
        # self.connection
        print(data)
