import timeit, time, sys
from Serial_process import *
from opencv import *
from Display import *
#from setting_ui import *

#https://glorypapa.tistory.com/18

class main:
    def __init__(self):
        self.img_por = img_process()
        self.Dis = DIs()
        self.Dis.start()
        self.SerPro = SerialProcess("COM12")

        self.LED_data = [7, 8]
        self.address_color = [[[0, 0, 0] for i in range(0, self.LED_data[1])] for i in range(0, self.LED_data[0])]
        self.SerPro.address_color = [[[0, 0, 0] for i in range(0, self.LED_data[1])] for i in range(0, self.LED_data[0])]
        self.SerPro.old_address_color = [[[0, 0, 0] for i in range(0, self.LED_data[1])] for i in range(0, self.LED_data[0])]
        self.img_por.address_color = [[[0, 0, 0] for i in range(0, self.LED_data[1])] for i in range(0, self.LED_data[0])]
        self.SerPro.start()


        self.prev_time = 0
        self.FPS_set = 30

    def run(self):
        while True:
            start_t = timeit.default_timer()

            current_time = start_t-self.prev_time
            if current_time > 1./self.FPS_set:
                for i, i_data in enumerate(self.address_color, 1):
                    if i == int(self.LED_data[0]/2)+1 or i == 1:
                        img = self.img_por.run2_cut(1 if i <=int(self.LED_data[0]/2) else 4)
                    self.img_por.run2(i, img)
                #cv2.imshow('original', )

                self.SerPro.write(self.img_por.address_color)

                self.prev_time = timeit.default_timer()

                FPS = int(1. / (self.prev_time - start_t))
                self.Dis.windowText_intput(F"{FPS}")

            #cv2.imshow('original', dat)

            # if cv2.waitKey(25) & 0xFF == ord('q'):
            #     cv2.destroyAllWindows()
            #     break

            time.sleep(0.0001)

def catch_exceptions(t, val, tb):
    old_hook(t, val, tb)

old_hook = sys.excepthook
sys.excepthook = catch_exceptions
if __name__ == "__main__":
    min = main()
    min.run()
