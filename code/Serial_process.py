import serial, time, threading


class SerialProcess(threading.Thread):
    def __init__(self, IMU_COM):
        threading.Thread.__init__(self)
        self.daemon = True
        self.COM_memo = IMU_COM
        self.connect(self.COM_memo)

        self.address_color = [[[0, 0, 0] for i in range(0, 8)] for i in range(0, 7)]
        self.old_address_color = [[[0, 0, 0]for i in range(0, 8)]for i in range(0, 7)]

        self.print_data = False
    def run(self):
        while True:
            try:
                for i, i_data in enumerate(self.address_color):
                    for o, o_data in enumerate(i_data):
                        for p, p_data in enumerate(o_data):
                            if p_data != self.old_address_color[i][o][p]:
                                data = (
                                    f"({i},{o},{int(o_data[0])},{int(o_data[1])},{int(o_data[2])})\n").encode()
                                if self.print_data:
                                    print(data)
                                self.serial_port.write(data)
                                buf = self.serial_port.readline().decode()
                                if self.print_data:
                                    print(buf)
                                self.old_address_color[i][o] = o_data
                time.sleep(0.0001)
            except:
                self.connect(self.COM_memo)
                time.sleep(1)

    def write(self, address_color):
        self.address_color = address_color

    def connect(self,COM_memo):
        while True:
            try:
                self.serial_port = serial.Serial(COM_memo, 250000, timeout=0.1)
                break
            except Exception as e:
                print("Check if the IMU connection port is", COM_memo)
                time.sleep(1)