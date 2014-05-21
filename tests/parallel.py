from multiprocessing import Pool
import timeit
from procol.console import print_err_trace

from catechu.http.client import CacheClient
from catechu.zeromq.client import ZeroMqCacheClient
from tests import caches


_cache_http = CacheClient(('127.0.0.1', 8087))


def _cache_parallel_test(fun, url, processes=5, numbers=10, times=1):
    def _pool_test():
        pool = Pool(processes)
        result = pool.map(fun, [url for i in range(numbers)])
        pool.close()
        return result

    return timeit.timeit(_pool_test, number=times)


def _get_mq_response(url):
    _cache_mq = ZeroMqCacheClient(('127.0.0.1', 9090))
    try:
        return _cache_mq.get_response(url)
    except:
        print_err_trace()


def _get_http_response(url):
    return _cache_http.get_response(url)


def test_parallel(url, times=10):
    #warmup
    _get_mq_response(url)
    _get_http_response(url)

    print 'Zero Mq: ', _cache_parallel_test(_get_mq_response, url, times=times, numbers=10)
    print
    print 'Http: ', _cache_parallel_test(_get_http_response, url, times=times, numbers=10)


def main():
    caches.remove_path()
    try:
        url = 'http://www.repubblica.it'

        test_parallel(url, times=10)
    finally:
        caches.remove_path()

if __name__ == '__main__':
    main()