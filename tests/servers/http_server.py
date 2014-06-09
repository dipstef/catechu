from httpy_cache import CacheConnect
import quecco.thread as quecco_thread

from catechu.http.server import serve as http_serve
from tests import TestCaches

#sqlite concurrent connections based on a thread producer-consumer queue
caches = TestCaches(connect=CacheConnect(connection=quecco_thread.connect))


def serve():
    http_serve(caches, port=8087)

if __name__ == '__main__':
    serve()