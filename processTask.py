import multiprocessing

class processTask:
    gcs = None
    def gps_worker(self):
        while True:
            status = self.gps.loop()
            latitude,longitude,altitude = self.gps.get_data()
            if status:
                print('Success: Set home position: | latitude:{} | longitude:{} | altitude:{}'.
                      format(latitude, longitude, altitude))
                self.mavlink.set_home_position(latitude, longitude, altitude)

    def transmit_worker(self):
        while True:
            gcs_data = self.gcs.read_data()
            copter_data = self.copter.read_data()
            self.gcs.write_data(copter_data)
            self.copter.write_data(gcs_data)

    def start(self):
        self.gps_work.start()
        self.transmit_work.start()

    def stop(self):
        self.gps_work.join()
        self.transmit_work.join()

    def __init__(self, gcs, copter, gps, mavlink):
        self.gcs = gcs
        self.copter = copter
        self.gps = gps
        self.mavlink = mavlink
        self.gps_work = multiprocessing.Process(target = self.gps_worker)
        self.transmit_work = multiprocessing.Process(target = self.transmit_worker)

