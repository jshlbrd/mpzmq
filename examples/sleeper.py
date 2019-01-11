import random
import time

from mpzmq import client
from mpzmq import server


class SleepWorker(server.Worker):
    """Worker that receives data from an mpzmq client through the mpzmq proxy,
    sleeps for a random amount of time, then sends the received data back as a
    result to client through the proxy. This example shows how to customize a
    worker and what happens if a worker does not respond in time.
    """
    def work(self, data):
        rand = random.randint(1, 5)
        time.sleep(rand)
        result = "{} result for {}".format(self.name, data.decode())
        return result


def main():
    """Starts an mpzmq proxy, 4 custom mpzmq workers (see class above), and an
    mpzmq client that sends 20 requests to the proxy. The client is configured
    with a timeout of 2500 milliseconds / 2.5 seconds -- this creates a scenario
    where workers may take longer to respond than the client is willing to
    wait.
    """
    proxy = server.Proxy()
    proxy.start()

    workers = []
    for _ in range(4):
        sw = SleepWorker()
        workers.append(sw)
        sw.start()

    c = client.Client(recv_timeout=2500)
    c.create_zmq()
    for i in range(20):
        response = c.request("{}!".format(i))
        if response:
            print("client: {}".format(response.decode()))
        else:
            print("client: server did not respond in time!")
    c.destroy_zmq()

    proxy.terminate()
    for worker in workers:
        worker.terminate()


if __name__ == "__main__":
    main()
