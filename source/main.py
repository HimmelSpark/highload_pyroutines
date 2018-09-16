import asyncio
import logging
import os

from source.config.config_parser import ConfigParser

forks = []


if __name__ == '__main__':
    config = ConfigParser.parse()

    logging.basicConfig(level=logging.INFO)

    for _ in range(0, int(config.cpu_count)):
        pID = os.fork()
        forks.append(pID)

        if pID == 0:
            loop = asyncio.get_event_loop()
            logging.INFO('running source with PID: {}'.format(int(os.getpid())))
            for _ in range(0, int(config.threads)):
                loop.create_task(launch_server(loop))

            try:
                loop.run_forever()
            except KeyboardInterrupt:
                logging.INFO('Server with PID {} closed by keyboard interrupt')
            finally:
                loop.stop() # но это неточно