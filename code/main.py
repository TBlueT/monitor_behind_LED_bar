import timeit, time
from Serial_process import *
from opencv import *
from Display import *
#LED bar pin
#GND
#DI
#vcc
#https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=chandong83&logNo=40183590328
class main:
    def __init__(self):
        self.img_por = img_process()
        self.Dis = DIs()
        self.Dis.start()
        self.SerPro = SerialProcess("COM12")
        self.SerPro.start()

        self.address_color = [[[0, 0, 0]for i in range(0, 8)]for i in range(0, 7)]

        self.prev_time = 0
        self.FPS_set = 30

    def run(self):
        while True:
            start_t = timeit.default_timer()

            current_time = start_t-self.prev_time
            if current_time > 1./self.FPS_set:
                for i in range(1, 7):
                    if i == 4 or i == 1:
                        img = self.img_por.run2_cut(1 if i <=3 else 4)
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


if __name__ == "__main__":
    min = main()
    min.run()
