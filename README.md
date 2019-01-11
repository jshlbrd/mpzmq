# mpzmq
This is a minimalist library for building scalable, distributed Python applications using ZeroMQ (ZMQ) and multiprocessing. The goal of this library is simplicity -- it is not a replacement for an API or RPC system, but it is a reliable, lo-fi alternative for when you need to offload Python processing to a multi-core remote server. The library is compatible with Python 2 and 3.

# mpzmq server
The mpzmq server performs two simultaneous tasks: it scales your Python code across multiple cores and creates a networked connection for your Python code to receive data across each core. The server library contains two components: a proxy that connects your code to the network and a worker that processes data sent to the proxy.

All data processing happens in two methods available in the worker: `init` and `work`. `init` is called once when the worker starts and is useful for setting up anything that is required during data processing; `work` is called each time the worker receives data and is where data processing happens. If your application requires client-defined arguments, then I suggest encoding the arguments with the data (e.g. as a [protocol buffer](https://developers.google.com/protocol-buffers/docs/pythontutorial)).

Note: server processes will run indefinitely and should be shutdown via process termination.

# mpzmq client
The mpzmq client performs one task: send data to and receive results from the configured mpzmq proxy. The client library includes an optional timeout that allows the client to skip waiting for a response from the server (this is useful in case the worker crashes or goes offline).
