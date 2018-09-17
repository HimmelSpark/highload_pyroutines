import asyncio
import logging
import os

from source.handler.executor import Executor
from source.server.server import Server
from source.config.config_parser import ConfigParser
from source.handler.handler import Handler

forks = []

if __name__ == '__main__':
    config = ConfigParser.parse()

    logger = logging.getLogger('server')

    for _ in range(0, int(config.cpu_count)):
        pID = os.fork()
        forks.append(pID)

        if pID == 0:
            loop = asyncio.get_event_loop()
            logger.debug('running source with PID: {0}'.format(str(os.getpid())))
            for _ in range(0, int(config.threads)):
                loop.create_task(
                    Server(
                        config,
                        loop,
                        Handler(config.root_dir, Executor(config)),
                        )
                    .launch_server()
                )
            loop.run_forever()


            # finally:
                # loop.stop()  # но это неточно

    for pID in forks:
        os.waitpid(pID, 0)