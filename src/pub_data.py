#!/usr/bin/env python
import rospy
from pyirobot import Robot
import json
from std_msgs.msg import String
from roomba980.msg import Mission

'''
robot_IP = ''
robot_password = ''

robot = Robot(robot_IP, robot_password)
'''
data = {'binStatus': 'Normal', 'readyStatus': 'Ready', 'robotPosition': {'theta': -79, 'point': {'y': -22, 'x': 2}}, 'robotStatus': 'charge', 'missionCoveredSquareFootage': 0, 'missionElapsedMinutes': 0, 'batteryPercentage': 100}
datajs = json.dumps(data, sort_keys=True, indent=4)
print(type(datajs))

def get_msg_data(data):
    miss_msg = Mission()
    miss_msg.batteryPercentage = str(data['batteryPercentage'])
    miss_msg.binStatus = data['binStatus']
    miss_msg.missionCoveredSquareFootage = str(data['missionCoveredSquareFootage'])
    miss_msg.missionElapsedMinutes = str(data['missionElapsedMinutes'])
    miss_msg.readyStatus = data['readyStatus']
    miss_msg.robotPositionXY[0] = data['robotPosition']['point']['x']
    miss_msg.robotPositionXY[1] = data['robotPosition']['point']['y']
    miss_msg.robotPositionAngle = data['robotPosition']['theta']
    miss_msg.robotStatus = data['robotStatus']
    return miss_msg


def talker():
    pub = rospy.Publisher('mission', Mission, queue_size=10)
    rospy.init_node('getMission', anonymous=True)
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        #data = robot.GetMission()
        mission_msg = get_msg_data(data)
        pub.publish(mission_msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
        