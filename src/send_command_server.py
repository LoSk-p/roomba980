#!/usr/bin/env python
import rospy
import json
from std_msgs.msg import String
from roomba980.msg import Mission
sys.path.insert(0, '/home/alena/Roomba980-Python/roomba')
from roomba import Roomba
file = open('/home/alena/roomba_wc/src/roomba980/src/config', 'r')
roomba_IP = file.readline()
roomba_blit = file.readline()
roomba_password = file.readline()
file.close()
roomba_IP = roomba_IP.split()[0]
roomba_blit = roomba_blit.split()[0]
roomba_password = roomba_password.split()[0]

'''
myroomba = Roomba(roomba_IP, roomba_blit, roomba_password)
'''

def send_command(command):
    if commamd == 'Start':
        #myroomba.send_command("start")
        rospy.loginfo('Starting cleaning')
    elif command == 'Stop':
        #myroomba.send_command("stop")
        rospy.loginfo('Stop cleaning')
    elif command == 'Home':
        #myroomba.send_command("dock")
        rospy.loginfo('Going back home')

def send_command_server():
    rospy.init_node('send_command_server')
    rospy.Service('send_command', String, send_command)
    rospy.spin()

if __name__ == '__main__':
    send_command_server()
