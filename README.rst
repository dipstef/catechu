Catechu
=======
Remote interface for the ``quiche`` http response cache.

Uses same ideas of ``requem`` for querying ``sqlite3`` database remotely.
For more info: https://github.com/dipstef/requem

Usage
=====
Same interface of https://github.com/dipstef/quiche

Connections
===========
Define a factory returning a cache connection given some params.
As an example we return a different cache for http domain.

.. code-block:: python

    import quiche
    from url.domain import get_domain

    class Caches(object):
        def get_cache(self, url, *args, **kwargs):
            cache = get_domain(url) + '.db'
            def quiche_connect():
                return quiche.connect(cache)
            return quiche_connect

    >>> caches = Caches()

Zeromq
======

``zeromq`` based server offers the best performance:


Server:
.. code-block:: python

    from catechu.zeromq import server

    >>> server.serve(caches, port=9090)


Client:

.. code-block:: python

    from catechu.zeromq.client import ZeroMqCacheClient
    from quiche import CacheOrClient

    cache = ZeroMqCacheClient(('server-address', 9090))
    client = CacheOrClient(cache)
    .....


Http
====

http based interface

Server:

.. code-block:: python

    from catechu.http import server

    >>> server.serve(caches, port=9090)

Client:

.. code-block:: python

    from catechu.http.client import CacheClient

    cache = CacheClient(('127.0.0.1', 8087))
    ....