import threading
from threading import Event
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

class Worker(threading.Thread):

    def __init__(self, e: Event):
        super().__init__()
        self.event = e

    def run(self):
        logging.debug('Worker waiting for event')
        while not self.event.is_set():
            self.event.wait()
        logging.debug('Worker got event. Exiting')


if __name__ == '__main__':
    event = Event()
    threads = []

    for i in range(4):
        thread = Worker(event)
        thread.start()
        threads.append(thread)

    time.sleep(2)
    event.set()

    for t in threads:
        t.join()