from torch import ShortTensor
import win32api
import win32con
import win32gui
import win32ui
import time
import cv2
from PIL import Image, ImageGrab
import numpy as np


def MoveTo(x, y):
    nx = int(x*65535/win32api.GetSystemMetrics(0))
    ny = int(y*65535/win32api.GetSystemMetrics(1))
    win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE |
                         win32con.MOUSEEVENTF_MOVE, nx, ny)


time.sleep(2)
l = [(330, 630), (330, 852), (325, 1074), (386, 667), (346, 1022),
     (387, 1399), (514, 350), (600, 615), (540, 960), (600, 1362), (516, 1665)]
w = [32, 32, 32, 72, 63, 72, 100, 180, 106, 190, 100]


class box:
    def __init__(self, center, len):
        self.xywh = [center[0]-len//2, center[1]-len//2, len, len]
        self.len = len
        self.state = 0
        self.shape = (len, len)
        self.center = center

    def get_self_img(self, img):
        self_img = img[self.xywh[0]:self.xywh[0] +
                       self.len, self.xywh[1]:self.xywh[1]+self.len]
        return self_img

    def update_state(self, img):
        self_img = self.get_self_img(img)
        hsv = cv2.cvtColor(self_img, cv2.COLOR_BGR2HSV)
        # 颜色识别(红色)，过滤红色区域
        lower_red1 = np.array([0, 43, 46])  # 红色阈值下界
        higher_red1 = np.array([10, 255, 255])  # 红色阈值上界
        mask_red1 = cv2.inRange(hsv, lower_red1, higher_red1)
        lower_red2 = np.array([156, 43, 46])  # 红色阈值下界
        higher_red2 = np.array([180, 255, 255])  # 红色阈值上界
        mask_red2 = cv2.inRange(hsv, lower_red2, higher_red2)
        mask_red = cv2.add(mask_red1, mask_red2)  # 拼接过滤后的mask
        pd_color = np.mean(mask_red)
        if pd_color < 150:  # 蓝色
            self.state = 1
            # cv2.imwrite(f'{np.random.randint(0,10)}.png',img)
        else:  # 红色
            self.state = 0


def window_capture():
    hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = 1920
    h = 1080
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    #saveBitMap.SaveBitmapFile(saveDC, filename)
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    # 生成图像
    im_PIL = Image.frombuffer(
        'RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
    return im_PIL


'''
box_list=[]
img=window_capture()
img=np.array(img)[:,:,::-1]
for i in range(11):
    box_list.append(box(l[i],w[i]))
    self_img=box_list[i].get_self_img(img)
    cv2.imwrite(f'{i}.png',self_img)
'''


def movetest():
    for i in range(11):
        mouse_move = (l[i][1]-960, l[i][0]-540)
        MoveTo(mouse_move[0]/39, mouse_move[1]/68)
     
        time.sleep(0.5)
        MoveTo(-mouse_move[0]/39, -mouse_move[1]/68)
        time.sleep(0.1)


def shoottest():
    for i in range(19):

        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        time.sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        time.sleep(0.05)
        MoveTo(0.02, 0.14)  # 压枪,第一个越大代表越往右压，第二个越大代表越往下压
        time.sleep(0.2)
def move_shoot_test(res):
    for j in range(7):
        for i in res:
            mouse_move = (l[i][1]-960, l[i][0]-540)

            MoveTo(mouse_move[0]/39, mouse_move[1]/68)

            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
            time.sleep(0.02)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
            time.sleep(0.08)

            MoveTo(-mouse_move[0]/39, -mouse_move[1]/68)
            time.sleep(0.1) 
            MoveTo(0.0295, 0.215)  # 压枪,第一个越大代表越往右压，第二个越大代表越往下压
            time.sleep(0.01)
res=[0,1]
move_shoot_test(res)
