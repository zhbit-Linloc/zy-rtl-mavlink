import time
import serial

timeout = 50


class GPS:
    serial = None
    latitude = 0
    longitude = 0
    altitude = 0
    altitude_msl = 0
    speedkm = 0
    gpsStatus = None


    def __init__(self, port, baudrate=9600):
        self.serial = serial.Serial(port=port, baudrate=baudrate)

    def get_status(self):
        if self.gpsStatus == 'A':
            return True
        return False

    def on_update_rmc(self):
        print("latitude: {}, longitude: {} | Speed (Km) is {}".format(self.latitude, self.longitude, self.speedkm))

    def on_update_gga(self):
        print("latitude: {}, longitude: {}, altitude: {}, alitude_msl: {}".format(self.latitude, self.longitude, self.altitude, self.altitude_msl))


    def on_error(self, msg):
        print("ERROR： {}".format(msg))

    def loop(self):
        if self.serial.in_waiting > 0:
            timeout_t = timeout
            stringAllLine = ""
            while timeout_t > 0:
                if self.serial.in_waiting > 0:
                    stringAllLine = stringAllLine + self.serial.readline().decode()

                    timeout_t = timeout
                else:
                    timeout_t = timeout_t - 1
                time.sleep(0.001)
            gps_list = stringAllLine.split('\r\n')
            # print(stringAllLine)
            for gps_item in gps_list:
                gps_info = gps_item.split(',')
                if len(gps_info) >= 12:
                    if gps_info[0] == '$GNRMC':
                        self.gpsStatus = gps_info[2]
                        if self.get_status():
                            # print(gps_info)
                            self.latitude = round(self.GPSTransforming(gps_info[3]), 6)
                            self.longitude = round(self.GPSTransforming(gps_info[5]), 6)
                            self.speedkm = round(float(gps_info[7]) * 1.852, 2)


                            self.on_update_rmc()
                        else:
                            self.on_error('定位无效\n%s' % gps_item)
                    if gps_info[0] == '$GPRMC':
                        print(gps_info)
                    if gps_info[0] == '$GNGGA':

                        print(gps_info)
                        if gps_info[6] == '1':
                            self.latitude = round(self.GPSTransforming(gps_info[2]), 6)
                            self.longitude = round(self.GPSTransforming(gps_info[4]), 6)
                            self.altitude = round(float(gps_info[9]) + float(gps_info[11]), 1)
                            self.altitude_msl = float(gps_info[9])

                            self.on_update_gga()

                    if gps_info[0] == '$GPGGA':
                        print(gps_info)

    def GPSTransforming(self, _Value):
        Ret = 0.0
        TempStr = _Value.split('.')
        x = TempStr[0][0: len(TempStr[0]) - 2]
        y = TempStr[0][len(TempStr[0]) - 2: len(TempStr[0])]
        z = TempStr[1][0: 4]
        Ret = float(x) + float(y) / 60 + float(z) / 600000
        return Ret

