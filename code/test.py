import sys
import numpy as np
from PyQt5 import uic
from PyQt5.QtWidgets import  *
from PyQt5.QtGui import QPainter, QPen, QPixmap, QColor
from PyQt5.QtCore import Qt
GUI_class = uic.loadUiType('setting_ui.ui')[0]

class Setting(QMainWindow, GUI_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.Zone_high = 10

        ##################################################################################################
        self.LED_amount.valueChanged.connect(self.LED_count_execution)

        ##################################################################################################
        self.display_view.resize(508,282)
        self.display_view_Count = [self.display_view.size().width(), self.display_view.size().height()]

        ##################################################################################################
        self.Zone_Count = self.LED_amount.value()
        self.Zone_Drawing = True

    def resizeEvent(self, event):
        self.display_view_Count = [self.display_view.size().width(), self.display_view.size().height()]
        self.LED_LED_count_Drawing()

    def LED_count_execution(self):
        self.Zone_Count = self.LED_amount.value()
        self.LED_LED_count_Drawing()

    def LED_LED_count_Drawing(self):
        x = 0
        y = 0
        w = int(self.display_view_Count[0]/self.Zone_Count)
        h = int(self.display_view_Count[1] / self.Zone_high)

        by = self.display_view_Count[1] - int(self.display_view_Count[1] / self.Zone_high)
        bh = self.display_view_Count[1]
        pixmap = QPixmap(self.display_view.size())
        pixmap.fill(Qt.transparent)
        qp = QPainter(pixmap)

        for i in range(0, self.Zone_Count):
            print(x,y,w,h, self.display_view_Count[0])
            qp.setBrush(QColor(255, 0, 0))
            qp.drawRect(x, y, w, h)

            qp.setBrush(QColor(0, 255, 0))
            qp.drawRect(x, by, w, bh)
            x = w
            w += int(self.display_view_Count[0]/self.Zone_Count)
        #
        # x = 0
        # y = int(self.display_view_Count[1] / self.Zone_high)
        # w = int(self.display_view_Count[0] / self.Zone_high-22)
        # h = int((self.display_view_Count[1]-(int(self.display_view_Count[1] / self.Zone_high)))/self.Zone_Count)
        #
        # for i in range(0, self.Zone_Count):
        #     qp.setBrush(QColor(0, 0, 255))
        #     qp.drawRect(x, y, w, h)
        #
        #     # qp.setBrush(QColor(0, 255, 0))
        #     # qp.drawRect(x, by, w, bh)
        #     y = h
        #     h -= int(self.display_view_Count[1] / self.Zone_high)
        # print(x, y, w, h, self.display_view_Count[1])
        qp.end()
        self.display_view.setPixmap(pixmap)

def catch_exceptions(t, val, tb):
    old_hook(t, val, tb)

old_hook = sys.excepthook
sys.excepthook = catch_exceptions

if __name__ == "__main__":
    app = QApplication(sys.argv)
    setting = Setting()
    setting.show()
    app.exec()