from contextlib import closing

import zmq
from httpy.http.response import HttpResponse
from catechu.zeromq import CacheCommand, context


class ZeroMqCacheClient(object):

    def __init__(self, address, cache_args):
        self._address = address
        self._cache_args = cache_args

    def get_response(self, url):
        return self._execute(CacheCommand.GET, url)

    def store(self, response):
        response = HttpResponse(response.request, response.url, response.status, response.headers, response.body)

        self._execute(CacheCommand.STORE, response.request.url, response)

    def _execute(self, command, url, response=None):
        with closing(context.socket(zmq.REQ)) as socket:
            socket.connect('tcp://{}:{}'.format(*self._address))

            socket.send_pyobj((self._cache_args, command, url, response))

            response = socket.recv_pyobj()
            return response
