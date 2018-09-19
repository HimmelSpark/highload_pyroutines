import asyncio
# import logging
import os
# import uvloop
from config.config_parser import ConfigParser
from handler.executor import Executor
from handler.handler import Handler
from server.server import Server
from multiprocessing import Process

procs = []


# forks = []
# if __name__ == '__main__':
#     config = ConfigParser.parse()
#
#     logger = logging.getLogger('server')
#
#     asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
#
#     for i in range(0, int(config.cpu_count)):
#         pID = os.fork()
#         forks.append(pID)
#
#         if pID == 0:
#             loop = asyncio.get_event_loop()
#             print('running source with PID: {0}'.format(str(os.getpid())))
#             for _ in range(0, int(config.threads)):
#                 loop.create_task(
#                     Server(
#                         config,
#                         loop,
#                         Handler(config.root_dir, Executor(config)),
#                         )
#                     .launch_server()
#                 )
#                 loop.run_forever()
#
#     for pID in forks:
#         os.waitpid(pID, 0)


def start():
    loop = asyncio.get_event_loop()
    print('running source with PID: {0}'.format(str(os.getpid())))
    for _ in range(0, int(config.threads)):
        handler = Handler(config.root_dir, Executor(config))
        server = Server(config=config, loop=loop, handler=handler)
        loop.create_task(server.launch_server())
    loop.run_forever()


if __name__ == '__main__':

    config = ConfigParser.parse()
    print('host: {}\nport: {}\n'.format(config.host, config.port))
    # asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    try:
        for _ in range(0, int(config.cpu_count)):
            procs.append(Process(target=start))

        for i in procs:
            i.start()

        for i in procs:
            i.join()

    except KeyboardInterrupt:
        for i in procs:
            i.terminate()
