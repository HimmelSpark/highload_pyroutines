import signal
from logging import info
from os import getpid

def closeHandler(loop):
    # info('closing e_loop: ', getpid())
    loop.remove_signal_handler(signal.SIGINT)
    loop.stop()


def startProcess(conf, sock):

    from handler.executor import Executor
    from handler.handler import Handler
    from server.server import Server
    from asyncio import get_event_loop



    loop = get_event_loop()
    loop.add_signal_handler(signal.SIGINT, closeHandler, loop)


    try:

        info('running source with PID {}'.format(str(getpid())))
        handler = Handler(conf.root_dir, Executor(conf.root_dir))
        for _ in range(0, int(conf.threads)):
            server = Server(config=conf, loop=loop, handler=handler, sock=sock)
            loop.create_task(server.launch_server())
        loop.run_forever()

    except Exception:
        loop.stop()
        info('stop loop {}'.format(getpid()))

    finally:
        loop.stop()
        info('stop loop {}'.format(getpid()))




def createProcesses():

    from logging import basicConfig, info, INFO
    from config.config_parser import ConfigParser
    from multiprocessing import Process
    from os import waitpid
    import socket


    procs = []

    config = ConfigParser.parse()
    basicConfig(level=INFO)
    info('\nhost: {}\nport: {}\nthreads: {}\ncpu_count: {}'.format(config.host, config.port, config.threads, config.cpu_count))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((config.host, int(config.port)))
    s.listen(100)

    try:
        for _ in range(0, int(config.cpu_count)):
            procs.append(Process(target=startProcess, args=([config, s])))

        for i in procs:
            i.start()

        for i in procs:
            waitpid(i.pid, 0)

    except KeyboardInterrupt:
        for i in procs:
            i.terminate()

createProcesses()
