import asyncio
# import uvloop
import os
import socket
import logging

from multiprocessing import Process

from config.config_parser import ConfigParser
from handler.executor import Executor
from handler.handler import Handler
from server.server import Server

procs = []

def start(conf, sock):
    loop = asyncio.get_event_loop()

    try:
        # asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
        logging.info('running source with PID {}'.format(str(os.getpid())))
        handler = Handler(conf.root_dir, Executor(conf.root_dir))
        for _ in range(0, int(conf.threads)):
            server = Server(config=conf, loop=loop, handler=handler, sock=sock)
            loop.create_task(server.launch_server())
        loop.run_forever()

    finally:
        print('stop loop', os.getpid())
        loop.stop()


if __name__ == '__main__':

    config = ConfigParser.parse()

    logging.basicConfig(level=logging.INFO)

    logging.info('\nhost: {}\nport: {}\nthreads: {}\ncpu_count: {}'.
                 format(config.host, config.port, config.threads, config.cpu_count))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((config.host, int(config.port)))

    try:
        for _ in range(0, int(config.cpu_count)):
            procs.append(Process(target=start, args=([config, s])))

        for i in procs:
            i.start()

        for i in procs:
            os.waitpid(i.pid, 0)

    except KeyboardInterrupt:
        for i in procs:
            i.terminate()
