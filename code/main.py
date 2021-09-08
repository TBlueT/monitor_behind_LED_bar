import numpy as np
import pyautogui as pg
import mss
import cv2
import timeit
from PIL import ImageGrab
from Serial_process import *
from opencv import *
from multiprocessing.pool import ThreadPool
#LED bar pin
#GND
#DI
#vcc


class main:
    def __init__(self):
        self.img_por = [None] * 7
        self.img = [None] * 7
        for i in range(len(self.img_por)):
            self.img_por[i-1] = img_process()
        self.SerPro = SerialProcess("COM12")
        self.SerPro.start()
        self.address_color = [[[0, 0, 0] for i in range(0, 8)], [[0, 0, 0] for i in range(0, 8)],
                              [[0, 0, 0] for i in range(0, 8)],
                              [[0, 0, 0] for i in range(0, 8)], [[0, 0, 0] for i in range(0, 8)],
                              [[0, 0, 0] for i in range(0, 8)]]
    def run(self):
        while True:
            start_t = timeit.default_timer()

            # screen = np.array(ImageGrab.grab())
            #
            # # image_pos = {'left': 0, 'top': 0, 'width': w_size[0], 'height': w_size[1]}
            # # with mss.mss() as sct:
            # #     image_pos1 = np.array(sct.grab(image_pos))[:, :, :3]
            # dst = cv2.resize(screen, dsize=(0, 0), fx=0.3, fy=0.3)
            # dst = cv2.cvtColor(dst,cv2.COLOR_BGR2RGB)
            # for i in range(1,4):
            #     self.img[i-1] = threading.Thread(target=self.img_por[i-1].run, args=(i,))
            #     self.img[i-1].start()
            # for i in range(1, 4):
            #     self.img[i-1].join()
            #     self.address_color[i-1] = self.img_por[i-1].address_color[i-1]
            for i in range(1, 7):
                self.address_color[i-1] = self.img_por[i - 1].run(i)


            self.SerPro.write(self.address_color)

            terminate_t = timeit.default_timer()
            FPS = int(1. / (terminate_t - start_t))
            print(F"\rFPS: {FPS}",end="")

            #cv2.imshow('original', dat)

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

            time.sleep(0.0001)


if __name__ == "__main__":
    min = main()
    min.run()
