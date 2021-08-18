from gps import GPS
from mavlink import mavLink
import argparse


def get_args():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--conn', '-n', default='/dev/ttyUSB0',
                        type=str,
                        help="Specify the file in which the model is stored")
    return parser.parse_args()


def main():
    master = mavLink(args.conn)
    master.sent_request(50)
    gps = GPS('/dev/ttyUSB0')

    while True:
        try:
            gps.loop()
            master.set_home_position(gps.latitude, gps.longitude, gps.altitude)
            master.get_mavmsg(['ATTITUDE', 'SYS_STATUS', 'HOME_POSITION'])
            # master.sent_request(50)
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    args = get_args()
    main()
