from quiche.zeromq import server
from tests import caches


def serve():
    server.serve(caches, port=9090, local=True)

if __name__ == '__main__':
    serve()