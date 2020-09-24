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

def send_command(command):
    if commamd == 'Start':
        #robot.StartCleaning()
        rospy.loginfo('Starting cleaning')
    elif command == 'Stop':
        #robot.StopCleaning()
        rospy.loginfo('Stop cleaning')
    elif command == 'Home':
        #robot.ReturnHome()
        rospy.loginfo('Going back home')

def send_command_server():
    rospy.init_node('send_command_server')
    rospy.Service('send_command', String, send_command)
    rospy.spin()

if __name__ == '__main__':
    send_command_server()
