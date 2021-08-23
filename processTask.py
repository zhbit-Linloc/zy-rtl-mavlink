# -*- encoding: utf-8 -*-
'''
@File    :   processTask.py
@Contact :   1045853428@qq.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/8/23 9:50   chenzishen     1.0        多进程任务

@Function:   None
'''


import multiprocessing

class processTask:
    # GPS工作
    def gps_worker(self):
        while True:
            status = self.gps.loop()    # 获取gps卫星信息，返回获取值的状态
            latitude,longitude,altitude = self.gps.get_data() # 获取经纬度和高度
            if status:
                print('Success: Set home position: | latitude:{} | longitude:{} | altitude:{}'.
                      format(latitude, longitude, altitude))
                self.mavlink.set_home_position(latitude, longitude, altitude)   # 给无人机设置home点位置

    # 透明传输
    def transmit_worker(self):
        while True:
            gcs_data = self.gcs.read_data()
            copter_data = self.copter.read_data()
            self.gcs.write_data(copter_data)
            self.copter.write_data(gcs_data)

    # 开始任务
    def start(self):
        self.gps_work.start()
        self.transmit_work.start()

    # 结束任务
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

