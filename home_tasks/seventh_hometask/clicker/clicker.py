from __future__ import absolute_import, division, print_function
import time
from functools import partial
from threading import Thread
import threading
import win32api, win32con
import time
import math
import sys
from queue import Queue
import win32api
import win32con
from pynput.mouse import Listener
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from design import Ui_Dialog
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication
from PyQt5.QtCore import QCoreApplication
import os


class ImageDialog(QtWidgets.QMainWindow, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # Make some local modifications.
        # self.colorDepthCombo.addItem("2 colors (1 bit per pixel)")

        # Connect up the buttons.

        self.ui.pushButton_4.clicked.connect(self._exit)
        self.ui.pushButton_2.clicked.connect(self.start)
        self.ui.pushButton.clicked.connect(self.record)
        # self.cancelButton.clicked.connect(self.reject)
    def _exit(self):
        sys.exit()

    def record(self):
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
                    python = sys.executable
                    os.execl(python, python, *sys.argv)

    def start(self):
        with open('log.txt', 'r') as log_file:
            line = log_file.readline()
            while line:
                if line == '\n':
                    continue
                coords = line.split(',')
                x = coords[0]
                qwerty = coords[1]

                qwerty = qwerty.split(' ')

                y = qwerty[0]
                try:
                    button = qwerty[1]
                    if 'left' in button:
                        left_click(int(x), int(y))
                    if 'right' in button:
                        right_click(int(x), int(y))
                    if 'mid' in button:
                        middle_click(int(x), int(y))
                except:
                    pass
                win32api.SetCursorPos((int(x), int(y)))
                time.sleep(.02)
                line = log_file.readline()

def main():
    app = QtWidgets.QApplication(sys.argv)
    myapp = ImageDialog()
    myapp.show()
    sys.exit(app.exec_())

def on_click(queue, x, y, button, pressed):
    if pressed:
        queue.put('{0},{1} {2}\n'.format(x, y, button))
        print(button)


def detect_clicks(queue):
    with Listener(on_click=partial(on_click, queue)) as listener:
        listener.join()


def track_movement(queue):
    while not win32api.GetAsyncKeyState(win32con.VK_ESCAPE):
    # while True:
        x, y = win32api.GetCursorPos()
        print(x, y)
        queue.put('{0},{1}\n'.format(x, y))
        time.sleep(0.01)

def left_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

def right_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)

def middle_click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, x, y, 0, 0)

if __name__ == '__main__':
    main()