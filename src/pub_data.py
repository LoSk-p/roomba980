#!/usr/bin/env python3
import rospy
import json
from std_msgs.msg import String
from roomba980.msg import Mission
from roomba980.srv import Command
import sys
import os
import yaml
dirname = os.path.dirname(__file__)
file = open(dirname + '/config.yaml')
content = file.read()
file.close()
config = yaml.load(content)
sys.path.insert(0, config["path"]["roomba_python"] + "/Roomba980-Python/roomba")
from roomba import Roomba

#myroomba = Roomba(config["roomba"]["IP"], config["roomba"]["blid"], config["roomba"]["password"])

data = {'name': 'robot', 'batPct': 100, 'cleanMissionStatus': {'cycle': 'none', 'phase': 'charge', 'error': 0, 'notReady': 0}, 'pose': {'point': {'x': 100, 'y': 20},'theta': -28}, 'audio': {'active': True}}
data_state = "Charging"

def send_command(req):
    if req.command == 'Start':
        #myroomba.send_command("start")
        return('Starting cleaning')
    elif req.command == 'Stop':
        #myroomba.send_command("stop")
        return('Stop cleaning')
    elif req.command == 'Home':
        #myroomba.send_command("dock")
        return('Going back home')
    else:
        return('Wrong command')

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
    rospy.Service('send_command', Command, send_command)
    pub = rospy.Publisher('mission', Mission, queue_size=10)
    rospy.init_node('getMission', anonymous=True)
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        #data_state = myroomba.current_state
        #data1 = myroomba.master_state
        #data = data1['state']['reported']
        mission_msg = get_msg_data(data, data_state)
        pub.publish(mission_msg)
        rate.sleep()


if __name__ == '__main__':
    try:
        #myroomba.connect()
        talker()
    except rospy.ROSInterruptException:
        pass
        