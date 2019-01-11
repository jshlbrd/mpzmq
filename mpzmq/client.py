import zmq


class Client(object):
    """Client that sends data to and receives results from an mpzmq proxy.

    Attributes:
        frontend: A string that contains the location and port of the mpzmq
            client-side proxy.
            Defaults to "127.0.0.1:5559".
        recv_timeout: An integer that controls how long (in milliseconds) to wait
            for a response from the mpzmq server.
            Defaults to -1 (waits forever).
    """
    def __init__(self, frontend="127.0.0.1:5559", recv_timeout=-1):
        """Inits Client with connection and polling settings."""
        self.frontend = frontend
        self.recv_timeout = recv_timeout

    def create_zmq(self):
        """Creates ZeroMQ connection to proxy."""
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.setsockopt(zmq.RCVTIMEO, self.recv_timeout)
        self.socket.setsockopt(zmq.REQ_CORRELATE, 1)
        self.socket.setsockopt(zmq.REQ_RELAXED, 1)
        self.socket.connect("tcp://{}".format(self.frontend))

    def destroy_zmq(self):
        """Shuts down ZeroMQ connection to proxy."""
        self.context.destroy()

    def request(self, data):
        """Sends data to and receives result from proxy."""
        if isinstance(data, str):
            data = data.encode()
        self.socket.send(data)

        try:
            return self.socket.recv()
        except zmq.error.Again:
            return None
