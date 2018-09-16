class Handler(object):
    def __init__(self, root):
        self.root = root

    async def handle(self, reader, writer):
        print(reader, writer)