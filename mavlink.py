from pymavlink import mavutil
from pymavlink.mavlink import MAVLink_request_data_stream_message, MAVLink_set_home_position_message, \
    MAVLink_home_position_message




class mavLink:
    def __init__(self, conn):
        self.conn = conn
        self.master = self.link_mav()

    def link_mav(self):
        master = mavutil.mavlink_connection(self.conn)
        master.wait_heartbeat()
        return master

    def sent_request(self, message_rate):
        self.master.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_ONBOARD_CONTROLLER,
                                       mavutil.mavlink.MAV_AUTOPILOT_INVALID, 1, 0, 0)
#        self.master.mav.send(MAVLink_request_data_stream_message(target_system=1, target_component=1, req_stream_id=10,
#                                                                req_message_rate=message_rate, start_stop=1))

    def set_home_position(self, latitude, longitude, altitude):
        # self.master.mav.send(MAVLink_home_position_message(latitude=0, longitude=0, altitude=0,
        #                                                    x=0.0, y=0.0, z=0.0, q=[1,1,1,1],
        #                                                    approach_x=0.0, approach_y=0.0, approach_z=0.0))
        latitude = int(latitude)
        longitude = int(longitude)
        altitude = int(altitude)
        self.master.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_ONBOARD_CONTROLLER,
                                       mavutil.mavlink.MAV_AUTOPILOT_INVALID, 1, 0, 0)
       
        self.master.mav.send(MAVLink_set_home_position_message(target_system=1,latitude=latitude, longitude=longitude, altitude=altitude,
                                                           x=0.0, y=0.0, z=0.0, q=[1, 1, 1, 1],
                                                           approach_x=0.0, approach_y=0.0, approach_z=0.0))

    def get_mavmsg(self, msg_type):
        try:
            msg = self.master.recv_match(type=msg_type, blocking=True)
            if not msg:
                raise ValueError()
            print(msg.to_dict())
            return msg.to_dict()
        except KeyboardInterrupt:
            print('Key bordInterrupt! exit')
            return

