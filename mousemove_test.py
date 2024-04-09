from win32 import win32api, win32gui, win32print
import win32con
import ctypes
from time import sleep

def MoveTo(x, y):
    nx = int(x*65535/win32api.GetSystemMetrics(0))
    ny = int(y*65535/win32api.GetSystemMetrics(1))
    win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE |
                         win32con.MOUSEEVENTF_MOVE, nx, ny)

sleep(2)
#ctypes.windll.user32.SetCursorPos(900, 540)
#win32api.SetCursorPos((900, 540))
for i in range(20):
    MoveTo(10,20)
    sleep(0.1)
    MoveTo(-10,-20)
    sleep(0.1)

