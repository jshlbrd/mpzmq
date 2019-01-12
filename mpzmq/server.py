import multiprocessing

import zmq


class Worker(multiprocessing.Process):
    """Worker that receives data from and sends results to an mpzmq proxy.

    Attributes:
        backend: A string that contains the location and port of the mpzmq
            worker-side proxy.
            Defaults to "127.0.0.1:5560".
    """
    def __init__(self, backend="127.0.0.1:5560"):
        """Inits Worker with connection settings."""
        super(Worker, self).__init__()
        self.backend = backend

    def run(self):
        """Connects to ZeroMQ proxy, runs user-defined init and work."""
        self.init()
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.connect("tcp://{}".format(self.backend))
        while 1:
            data = socket.recv()
            result = self.work(data)
            if isinstance(result, str):
                result = result.encode()
            socket.send(result)

    def init(self):
        """User-defined process initialization."""
        pass

    def work(self, data):
        """User-defined data processing."""
        return b""


class Proxy(multiprocessing.Process):
    """Proxy that connects mpzmq clients to mpzmq workers.

    Attributes:
        frontend_port: An integer that contains the port that the proxy should
            listen for client connections on.
            Defaults to 5559.
        backend_port: An integer that contains the port that the proxy should
            listen for worker connections on.
            Defaults to 5560.
    """
    def __init__(self, frontend_port=5559, backend_port=5560):
        """Inits Proxy with connection settings."""
        super(Proxy, self).__init__()
        self.frontend_port = frontend_port
        self.backend_port = backend_port

    def run(self):
        """Runs ZeroMQ proxy for connections between clients and workers."""
        context = zmq.Context()
        frontend = context.socket(zmq.XREP)
        frontend.bind("tcp://*:{}".format(self.frontend_port))
        backend = context.socket(zmq.XREQ)
        backend.bind("tcp://*:{}".format(self.backend_port))
        zmq.proxy(frontend, backend)
