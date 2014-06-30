from quice import CacheConnect
import quecco

from catechu.http.server import serve as http_serve
from tests import TestCaches

#sqlite concurrent connections based on a thread producer-consumer queue
caches = TestCaches(connect=CacheConnect(connection=quecco.threads))


def serve():
    http_serve(caches, port=8087)

if __name__ == '__main__':
    serve()