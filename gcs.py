import serial


class GCS:
    serial = None

    def __init__(self, port, baudrate=115200, timeout=0.001):
        self.serial = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)

    def read_data(self):
        return self.serial.readline()

    def write_data(self, data):
        self.serial.write(data)

if __name__ == '__main__':
    ser = serial.Serial(port='com4',baudrate=115200)
    while 1:
        data = ser.readline()
        print(data)
        ser.write(data)
