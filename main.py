from gps import GPS
from mavlink import mavLink
from gcs import GCS
import argparse
import serial
import threading
class myThread(threading.Thread):
    def __init__(self, threadID, gps):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.gps = gps
        
    def run(self):
        while True:
            self.gps.loop()
            #a_data = self.a.read_data()
            #print('{}'.format(a_data))
            #self.b.write_data()


def get_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--conn', '-n', default='/dev/ttyUSB0',
                        type=str,
                        help="Specify the file in which the model is stored")
    return parser.parse_args()


def main():
    master = mavLink(args.conn)
    master.sent_request(50)
    gps = GPS('/dev/ttyUSB1')

    gcs = GCS('/dev/ttyS0')
    copter = GCS('/dev/ttyUSB0')
    #gcs = serial.Serial(port='/dev/ttyS0',baudrate=115200,timeout=0.001)
    #copter = serial.Serial(port='/dev/ttyUSB0',baudrate=115200,timeout=0.001)
    thread = myThread(1, gps)
    thread.start()
    #thread1 = myThread(1, gcs, copter)
    #thread2 = myThread(2, copter, gcs)
    
    #thread1.start()
    #thread2.start()
    i = 100
    while True:
        try:
            gcs_data = gcs.read_data()
            #print('gcs: {}'.format(gcs_data))
            copter_data = copter.read_data()
            #print('copter: {}'.format(copter_data))
            gcs.write_data(copter_data)
            copter.write_data(gcs_data)
            #gps.loop()
            if i == 0:
                print('Success: Set home position')
                master.set_home_position(gps.latitude, gps.longitude, gps.altitude)
                i = 100
            i -= 1 
            #master.get_mavmsg(['ATTITUDE', 'SYS_STATUS', 'HOME_POSITION', 'HEARTBEAT'])
            #master.sent_request(50)
        except KeyboardInterrupt:
            thread.join()
            #thread2.join()
            break


if __name__ == '__main__':
    args = get_args()
    main()
