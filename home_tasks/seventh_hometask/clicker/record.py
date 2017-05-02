from __future__ import absolute_import, division, print_function
import time
from functools import partial
from threading import Thread
import threading
import sys
from queue import Queue
import win32api
import win32con
from pynput.mouse import Listener


def on_click(queue, x, y, button, pressed):
    if pressed:
        queue.put('{0},{1} {2}\n'.format(x, y, button))
        print(button)


def detect_clicks(queue):
    with Listener(on_click=partial(on_click, queue)) as listener:
        listener.join()


def track_movement(queue):
    while not win32api.GetAsyncKeyState(win32con.VK_ESCAPE):
        x, y = win32api.GetCursorPos()
        print(x, y)
        queue.put('{0},{1}\n'.format(x, y))
        time.sleep(0.01)



if __name__ == '__main__':
    queue = Queue()

    for function in [detect_clicks, track_movement]:
        thread = Thread(target=function, args=[queue])
        thread.daemon = True
        thread.start()
    with open('log.txt', 'w') as log_file:
        while True:
            log_file.write(queue.get())
            if win32api.GetAsyncKeyState(win32con.VK_SPACE):
                log_file.close()
                #


    #
    #
    #         log_file.write(queue.get())