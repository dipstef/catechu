import zmq
from . import CacheCommand


class CacheWorker(object):

    def __init__(self, caches, port, local=False):
        self.host = self.host = '127.0.0.1' if local else '0.0.0.0'
        self.port = port
        self._caches = caches
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REP)

    def start(self):
        self._socket.bind('tcp://{}:{}'.format(self.host, self.port))
        while True:
            cache_args, command, url, response = self._socket.recv_pyobj()

            cache = self._caches.get_cache(url, *cache_args)

            if command == CacheCommand.GET:
                response = cache.get_response(url)
                self._socket.send_pyobj(response)
            elif command == CacheCommand.STORE:
                cache.store(response)
                self._socket.send_pyobj('OK')
            else:
                self._socket.send('COMMAND UNKNOWN')

    def close(self):
        self._socket.close()
        self._caches.close()


def serve(caches, port=9090, local=False):
    print 'Cache Server, serving on ', port

    cache_service = CacheWorker(caches, port, local)
    try:
        cache_service.start()
    except (KeyboardInterrupt, SystemExit):
        cache_service.close()