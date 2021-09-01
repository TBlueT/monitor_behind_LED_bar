import cv2

class img_process:
    def __init__(self):
        self.address_color = [[[0, 0, 0] for i in range(0, 8)], [[0, 0, 0] for i in range(0, 8)],
                              [[0, 0, 0] for i in range(0, 8)],
                              [[0, 0, 0] for i in range(0, 8)], [[0, 0, 0] for i in range(0, 8)],
                              [[0, 0, 0] for i in range(0, 8)]]

    def image_cut(self, address, img):
        order = 1 if address == 1 else 4 if address == 2 else 7 if address == 3 else 1 if address == 4 else 4 if address == 5 else 7 if address == 6 else 0
        monitor_size = [len(img[0]), len(img)]

        x = int(monitor_size[0]/9*order)
        y = 0 if address <= 3 else monitor_size[1]-int(monitor_size[1]/30)
        h = int(monitor_size[0]/9*order+(monitor_size[0]/50))
        w = int(monitor_size[1]/30) if address <= 3 else monitor_size[1]
        for i in range(0, 8):
            roi = img[y:w,x:h]
            self.address_color[address-1][i] = self.color_average(roi)
            #img = cv2.rectangle(img, (x, y), (h, w), self.address_color[address-1][i], -1)
            x=h
            h+= int(monitor_size[0] / 50)

        return img

    def color_average(self, img):
        color = [0.0, 0.0, 0.0]
        count = 0.0
        for i in img:
            for o in i:
                for p in range(0,3):
                    count += 1.0
                    color[p] = (color[p]*(count-1)+o[p])/count
        return color