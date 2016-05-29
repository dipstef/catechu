import atexit
import os
import quiche


cache_path = os.path.join(os.path.dirname(__file__), 'cache.db')


class TestCaches(object):

    def __init__(self, connect=quiche.connect):
        self._cache = None
        atexit.register(self.close)
        self._connect = connect

    # Can return a different cache for each domain for instance
    def get_cache(self, url, *args, **kwargs):
        if not self._cache or not os.path.exists(cache_path):
            self._cache = self._connect(cache_path)
        return self._cache

    def close(self):
        if self._cache:
            self._cache.close()
        self.remove_path()

    def remove_path(self):
        if os.path.exists(cache_path):
            os.remove(cache_path)

caches = TestCaches()