from contextlib import closing

import zmq
from httpy.response import HttpResponse


class ZeroMqCacheClient(object):

    def __init__(self, reader_address, writer_address, *cache_args):
        self._context = zmq.Context()

        self._result_address = reader_address
        self._store_address = writer_address

        self._cache_args = cache_args

        self._store_socket = self._context.socket(zmq.PUSH)
        self._store_socket.connect('tcp://{}:{}'.format(*writer_address))

    def get_response(self, url):
        with closing(self._context.socket(zmq.REQ)) as socket:
            socket.connect('tcp://{}:{}'.format(*self._result_address))

            socket.send_pyobj((url, self._cache_args))

            response = socket.recv_pyobj()
            return response

    def store(self, response):
        response = HttpResponse(response.request, response.url, response.status, response.headers, response.body)

        self._store_socket.send_pyobj((response, self._cache_args))