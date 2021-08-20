from gps import GPS
from mavlink import mavLink
from gcs import GCS
import argparse
from processTask import processTask


def gps_worker(gps):
    while True:
        gps.loop()


def write_worker(gcs, copter, gps, master):
    i = 100
    while True:
        gcs_data = gcs.read_data()
        copter_data = copter.read_data()
        gcs.write_data(copter_data)
        copter.write_data(gcs_data)
        if i == 0:
            print('Set home position: | latitude:{} | longitude:{} | altitude:{}'.
                  format(gps.latitude, gps.longitude, gps.altitude))
            master.set_home_position(gps.latitude, gps.longitude, gps.altitude)
            i = 100
        i -= 1


def get_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--copter', '-c', default='/dev/ttyUSB0',
                        type=str,
                        help="设置无人机的端口号")
    parser.add_argument('--gps', '-gps', default='/dev/ttyUSB1',
                        type=str,
                        help="设置gps的端口号")
    parser.add_argument('--gcs', '-gcs', default='/dev/ttyUSB2',
                        type=str,
                        help="设置地面站的端口号")
    return parser.parse_args()


def main():
    master = mavLink(args.copter)
    master.sent_request(50)
    gps = GPS(args.gps)
    gcs = GCS(args.gcs)
    copter = GCS(args.copter)

    task = processTask(gcs=gcs, copter=copter, gps=gps, mavlink=master)
    try:
        task.start()
    except KeyboardInterrupt:
        task.stop()


if __name__ == '__main__':
    args = get_args()
    main()
