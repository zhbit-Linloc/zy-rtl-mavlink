from gps import GPS
from mavlink import mavLink
from gcs import GCS
import argparse
from processTask import processTask

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
