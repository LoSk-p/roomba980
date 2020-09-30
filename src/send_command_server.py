#!/usr/bin/env python3
import rospy
import json
from std_msgs.msg import String
from roomba980.msg import Mission
from roomba980.srv import Command
import sys
file = open('config', 'r')
sys.path.insert(0, '/home/alena/Roomba980-Python/roomba')
from roomba import Roomba


roomba_IP = file.readline()
roomba_blit = file.readline()
roomba_password = file.readline()
file.close()
roomba_IP = roomba_IP.split()[0]
roomba_blit = roomba_blit.split()[0]
roomba_password = roomba_password.split()[0]


myroomba = Roomba(roomba_IP, roomba_blit, roomba_password)


def send_command(req):
    #print(req.command)
    myroomba.connect()
    if req.command == 'Start':
        myroomba.send_command("start")
        return('Starting cleaning')
    elif req.command == 'Stop':
        myroomba.send_command("stop")
        return('Stop cleaning')
    elif req.command == 'Home':
        myroomba.send_command("dock")
        return('Going back home')
    else:
        return('Wrong command')
    myroomba.disconnect()

def send_command_server():
    rospy.init_node('send_command_server')
    rospy.Service('send_command', Command, send_command)
    rospy.spin()

if __name__ == '__main__':
    send_command_server()
