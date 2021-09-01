import numpy as np
from PIL import ImageGrab
from Serial_process import *
from opencv import *

#LED bar pin
#GND
#DI
#vcc

class main:
    def __init__(self):
        self.img_por = img_process()
        self.SerPro = SerialProcess("COM12")
        self.SerPro.start()
    def run(self):
        while True:

            screen = np.array(ImageGrab.grab())
            dst = cv2.resize(screen, dsize=(0, 0), fx=0.3, fy=0.3)
            for i in range(1,7):
                setattr(self,"img"+str(i), threading.Thread(target=self.img_por.image_cut, args=(i, dst)))
                getattr(self,"img"+str(i)).start()
            for i in range(1, 7):
                getattr(self, "img"+str(i)).join()

            self.SerPro.write(self.img_por.address_color)

            #cv2.imshow('original', cv2.cvtColor(dst, cv2.COLOR_BGR2RGB))

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

            #time.sleep(0.05)



if __name__ == "__main__":
    min = main()
    min.run()
