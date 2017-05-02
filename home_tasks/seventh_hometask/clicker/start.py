import win32api, win32con
import time
import math
import sys

def left_click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def right_click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)

def middle_click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP,x,y,0,0)


with open('log.txt', 'r') as log_file:
    line = log_file.readline()
    while line:
        if line=='\n':
            continue
        coords = line.split(',')
        x = coords[0]
        qwerty = coords[1]

        qwerty = qwerty.split(' ')

        y = qwerty[0]
        try:
            button = qwerty[1]
            if 'left' in button:
                left_click(int(x),int(y))
            if 'right' in button:
                right_click(int(x),int(y))
            if 'mid' in button:
                middle_click(int(x),int(y))
        except:
            pass
        win32api.SetCursorPos((int(x),int(y)))
        time.sleep(.02)
        line = log_file.readline()

