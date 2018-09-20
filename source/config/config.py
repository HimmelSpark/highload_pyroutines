# TODO: разобраться с передачей в конструктор 'None'
# TODO: почему не применяется значение по умолчанию


class Config(object):
    def __init__(self, host='0.0.0.0', port=8000, cpu_count=4, threads=20, root_dir='/var/www/html'):
        if host is None:
            self._host = '0.0.0.0'
        else:
            self._host = host

        if port is None:
            self._port = 80
        else:
            self._port = port

        if cpu_count is None:
            self._cpu_count = 4
        else:
            self._cpu_count = cpu_count

        if threads is None:
            self._threads = 20
        else:
            self._threads = threads

        if root_dir is None:
            self._root_dir = '/var/www/html'
        else:
            self._root_dir = root_dir

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def cpu_count(self) -> int:
        return self._cpu_count

    @property
    def threads(self) -> int:
        return self._threads

    @property
    def root_dir(self) -> str:
        return self._root_dir
