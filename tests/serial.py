import timeit

from quiche.http.client import CacheClient
from quiche.zeromq.client import ZeroMqCacheClient
from tests import caches


_cache_mq = ZeroMqCacheClient(('127.0.0.1', 9090))
_cache_http = CacheClient(('127.0.0.1', 8087))


def _cache_mq_test(url, times=1):
    def _pool_test():
        return _cache_mq.get(url)
    return timeit.timeit(_pool_test, number=times)


def _cache_http_test(url, times=1):
    def _pool_test():
        return _cache_http.get(url)
    return timeit.timeit(_pool_test, number=times)


def test_serial(url, times=100):
    # warmup
    _cache_mq.get(url)
    _cache_http.get(url)

    print 'Zero Mq: ', _cache_mq_test(url, times=times)
    print
    print 'Http:', _cache_http_test(url, times=times)


def main():
    caches.remove_path()
    try:
        url = 'http://www.repubblica.it'

        test_serial(url, times=100)
    finally:
        caches.remove_path()

if __name__ == '__main__':
    main()