import serial


class GCS:
    serial = None

    def __init__(self, port, baudrate=115200, timeout=0.001):
        self.serial = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)

    def read_data(self):
        return self.serial.readline()

    def write_data(self, data):
        self.serial.write(data)

def main():
    gcs = GCS(port='/dev/ttyUSB0',baudrate=115200)
    copter = GCS(port='/dev/ttyS0',baudrate=115200)
    while 1:
        gcs_data = gcs.read_data()
        copter_data = copter.read_data()
        print('gcs: {}'.format(gcs_data))
        print('copter: {}'.format(copter_data))
        gcs.write_data(copter_data)
        copter.write_data(gcs_data)

if __name__ == '__main__':
    main()
