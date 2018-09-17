import logging

from source.config.config import Config


class ConfigParser(object):
    @staticmethod
    def parse() -> Config:
        # / etc / httpd.conf
        data = {}
        try:
            with open('/Users/petrosadaman/Documents/kaka.conf') as config_file:
                for line in config_file:
                    if not line:
                        continue
                    pair = line.strip().split(' ')
                    key: str = pair[0]
                    try:
                        value: str = pair[1]
                        data.update({key: value})
                    except IndexError:
                        logging.debug('Config param "{0}" not provided'.format(key))

                return Config(
                    host=data.get('host'),
                    port=data.get('port'),
                    cpu_count=data.get('cpu_count'),
                    threads=data.get('threads'),
                    root_dir=data.get('root_dir')
                )

        except FileNotFoundError:
            return Config()
