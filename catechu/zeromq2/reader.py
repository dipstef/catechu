import zmq


class CacheResponseWorker(object):

    def __init__(self, caches, port, local=False):
        self.host = self.host = '127.0.0.1' if local else '0.0.0.0'
        self.port = port
        self._caches = caches
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REP)

    def start(self):
        self._socket.bind('tcp://{}:{}'.format(self.host, self.port))
        while True:
            url, cache_args = self._socket.recv_pyobj()
            cache = self._caches.get_cache(url, *cache_args)
            response = cache.get_response(url)

            self._socket.send_pyobj(response)

    def close(self):
        self._socket.close()
        self._caches.close()


def serve(caches, port=9091, local=False):
    print 'Serving on ', port

    cache_service = CacheResponseWorker(caches, port, local)
    try:
        cache_service.start()
    except (KeyboardInterrupt, SystemExit):
        cache_service.close()