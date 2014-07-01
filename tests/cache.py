from quiche import CacheOrClient
from quiche.cache import CachedHttpResponse

from catechu.zeromq.client import ZeroMqCacheClient

from catechu.http.client import CacheClient
from tests import caches


def _test_cache(cache, url):
    caches.remove_path()

    client_cache = CacheOrClient(cache)

    try:
        response = client_cache.get(url)
        assert not isinstance(response, CachedHttpResponse)
        retrieve_date = response.date

        response = client_cache.get(url)

        assert isinstance(response, CachedHttpResponse)
        assert response.date == retrieve_date
    finally:
        caches.remove_path()


def _test_zero_mq():
    print 'Testing Zero-Mq'
    #Start zero-mq worker
    cache = ZeroMqCacheClient(('127.0.0.1', 9090))
    _test_cache(cache, 'http://www.repubblica.it')


def _test_http():
    print 'Testing Http'
    #Start http server
    cache = CacheClient(('127.0.0.1', 8087))
    _test_cache(cache, 'http://www.repubblica.it')


def main():
    _test_zero_mq()
    _test_http()

if __name__ == '__main__':
    main()