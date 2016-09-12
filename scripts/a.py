import time
import json
import sys
import os

class MonitorTraffic(object):
    def __init__(self):
        self.card_name = 'eth0'
        self.warning_threshold = 20
        self.critical_threshold = 30
        self.file_path = "/tmp/"+self.card_name+'_monitor.tmp'

    def get_traffic_data(self):
        fd = open("/proc/net/dev", "r")
        for line in fd.readlines():
            if line.find(self.card_name) > 0:
                field = line.split()
                recv = field[1]
                send = field[9]
        fd.close()
        self.current_data = (time.time(),float(recv), float(send))
        if not os.path.isfile(self.file_path):
            self.save_current_data()


    def save_current_data(self):
        with open(self.file_path,'w') as f:
            json.dump(self.current_data, f)

    def get_file_data(self):
        with open(self.file_path,'r') as f:
            self.data_from_file = json.load(f)

    def judge_result(self):
        last_time , last_recv,last_send = self.data_from_file
        current_time,current_recv,current_send = self.current_data
        time_range = current_time-last_time
        if int(time_range) == 0:return
        recv_bps = (current_recv-last_recv)/1024/1024/time_range
        recv_bps = round(recv_bps,2)
        send_bps = (current_send-last_send)/1024/1024/time_range
        send_bps = round(send_bps,2)
        ret =  "- The Traffic In is %sMbps, Out is %sMbps. The Check Interval is %ds |In=%sMbps;%d;%d;0;0 Out=%sMbps;%d;%d;0;0" % (
                recv_bps,
                send_bps,
                time_range,
                recv_bps,
                self.warning_threshold,
                self.critical_threshold,
                send_bps,
                self.warning_threshold,
                self.critical_threshold,
            )
        if recv_bps > self.critical_threshold or send_bps > self.critical_threshold:
            ret = 'CRITICAL '+ret
            sys.exit(2)
        elif  recv_bps > self.warning_threshold or send_bps > self.warning_threshold:
            ret = 'WARNING '+ret
            sys.exit(1)
        else:
            ret = 'OK '+ret
        print ret


    def run(self):
        self.get_traffic_data()
        self.get_file_data()
        self.save_current_data()
        self.judge_result()


# get_handler = MonitorTraffic()
# get_handler.run()