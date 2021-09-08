import win32gui
import win32ui
import win32con
import cv2
import numpy as np
from PIL import Image

class img_process:
    def __init__(self):
        self.address_color = [[[0, 0, 0] for i in range(0, 8)], [[0, 0, 0] for i in range(0, 8)],
                              [[0, 0, 0] for i in range(0, 8)],
                              [[0, 0, 0] for i in range(0, 8)], [[0, 0, 0] for i in range(0, 8)],
                              [[0, 0, 0] for i in range(0, 8)]]

        self.hwnd = win32gui.GetDesktopWindow()
        self.size_x, self.size_y, self.size_h, self.size_w = win32gui.GetWindowRect(self.hwnd)



    def image_cut(self, address, img):
        order = 1 if address == 1 else 4 if address == 2 else 7 if address == 3 else 1 if address == 4 else 4 if address == 5 else 7 if address == 6 else 0
        monitor_size = [self.size_h, self.size_w]

        x = int(monitor_size[0]/9*order)
        y = 0 if address <= 3 else monitor_size[1]-int(monitor_size[1]/25)
        h = int(monitor_size[0]/9*order+(monitor_size[0]/50))
        w = int(monitor_size[1]/25) if address <= 3 else monitor_size[1]
        for i in range(0, 8):
            roi = img[y:w,x:h]
            self.address_color[address-1][i] = self.color_average(roi)
            #img = cv2.rectangle(img, (x, y), (h, w), self.address_color[address-1][i], -1)
            x=h
            h+= int(monitor_size[0] / 50)


    def color_average(self, img):
        color = sum(sum(img, [0, 0, 0]))
        #print((len(img[1]) * len(img)))
        return color/ (len(img[1]) * len(img))

    def read_Desktop(self, x,y,w,h):
        hDC = win32gui.GetWindowDC(self.hwnd)
        myDC = win32ui.CreateDCFromHandle(hDC)
        newDC = myDC.CreateCompatibleDC()

        myBitMap = win32ui.CreateBitmap()
        myBitMap.CreateCompatibleBitmap(myDC, w-x, h-y)

        newDC.SelectObject(myBitMap)

        newDC.BitBlt((-x, -y), (w, h), myDC, (0, 0), win32con.SRCCOPY)
        myBitMap.Paint(newDC)

        bmpinfo = myBitMap.GetInfo()
        bmpstr = myBitMap.GetBitmapBits(True)

        win32gui.DeleteObject(myBitMap.GetHandle())
        newDC.DeleteDC()
        myDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hDC)

        bmp = Image.frombytes('RGBA', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr)
        img = np.array(bmp)
        dst = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)

        return dst

    def run(self, address):
        order = 1 if address == 1 else 4 if address == 2 else 7 if address == 3 else 1 if address == 4 else 4 if address == 5 else 7 if address == 6 else 0
        monitor_size = [self.size_h, self.size_w]

        x = int(monitor_size[0] / 9 * order)
        y = 0 if address <= 3 else monitor_size[1] - int(monitor_size[1] / 25)
        h = int(monitor_size[0] / 9 * order + (monitor_size[0] / 50))
        w = int(monitor_size[1] / 25) if address <= 3 else monitor_size[1]

        roi1 = self.read_Desktop(x, y, h + (51 * 7), w)
        x = 0
        h = int((len(roi1[0])/9))
        y = 0
        w = int(monitor_size[1] / 25) if address <= 3 else len(roi1)
        for i in range(0, 8):
            #print(len(roi1[0]), x,y,h,w)
            roi = roi1[y:w,x:h]
            self.address_color[address - 1][i] = self.color_average(roi)
            # img = cv2.rectangle(img, (x, y), (h, w), self.address_color[address-1][i], -1)
            x = h
            h += int((len(roi1[0])/9))
        return self.address_color[address - 1]