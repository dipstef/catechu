import zmq


class CacheStoreWorker(object):

    def __init__(self, caches, port, local=False):
        self.host = self.host = '127.0.0.1' if local else '0.0.0.0'
        self.port = port
        self._caches = caches

        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PULL)

    def start(self):
        self._socket.bind('tcp://{}:{}'.format(self.host, self.port))
        while True:
            response, cache_args = self._socket.recv_pyobj()

            cache = self._caches.get_cache(response.url, *cache_args)
            cache.store(response)

    def close(self):
        self._socket.close()
        self._caches.close()


def serve(caches, port=9092, local=False):
    print 'Serving on ', port
    cache_services = CacheStoreWorker(caches, port, local=local)
    try:
        cache_services.start()
    except (KeyboardInterrupt, SystemExit):
        cache_services.close()