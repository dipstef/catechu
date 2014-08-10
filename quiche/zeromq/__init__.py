import zmq


class CacheCommand(object):
    GET, STORE = range(2)


context = zmq.Context()
