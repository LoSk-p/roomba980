#!/usr/bin/env python3
import rospy
import json
from std_msgs.msg import String
from roomba980.msg import Mission
import sys
file = open('/src/config', 'r')
sys.path.insert(0, '/home/alena/Roomba980-Python/roomba')
from roomba import Roomba

#file = open('/home/alena/roomba_wc/src/roomba980/src/config', 'r')
roomba_IP = file.readline()
roomba_blit = file.readline()
roomba_password = file.readline()
file.close()
roomba_IP = roomba_IP.split()[0]
roomba_blit = roomba_blit.split()[0]
roomba_password = roomba_password.split()[0]


myroomba = Roomba(roomba_IP, roomba_blit, roomba_password)

#data = {'name': 'robot', 'batPct': 100, 'cleanMissionStatus': {'cycle': 'none', 'phase': 'charge', 'error': 0, 'notReady': 0}, 'pose': {'point': {'x': 100, 'y': 20},'theta': -28}, 'audio': {'active': True}}
#data_state = "Charging"

def get_msg_data(data, data_state):
    miss_msg = Mission()
    miss_msg.name = data['name']
    miss_msg.batteryPercentage = str(data['batPct'])
    miss_msg.mission_cycle = data['cleanMissionStatus']['cycle']
    miss_msg.mission_phase = data['cleanMissionStatus']['phase']
    miss_msg.current_state = data_state
    miss_msg.error = str(data['cleanMissionStatus']['error'])
    miss_msg.mission_notReady = str(data['cleanMissionStatus']['notReady'])
    miss_msg.robotPositionXY[0] = data['pose']['point']['x']
    miss_msg.robotPositionXY[1] = data['pose']['point']['y']
    miss_msg.robotPositionAngle = data['pose']['theta']
    miss_msg.audio = str(data['audio']['active'])
    return(miss_msg)


def talker():
    pub = rospy.Publisher('mission', Mission, queue_size=10)
    rospy.init_node('getMission', anonymous=True)
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        myroomba.connect()
        data_state = myroomba.current_state
        data1 = myroomba.master_state
        data = data1['state']['reported']
        mission_msg = get_msg_data(data, data_state)
        pub.publish(mission_msg)
        myroomba.disconnect()
        rate.sleep()


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
        