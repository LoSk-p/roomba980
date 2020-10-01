#!/usr/bin/env python
import rospy
import json
from std_msgs.msg import String
from roomba980.msg import Mission
from roomba980.srv import Command
import subprocess
import os
import time
import ipfshttpclient

roomba_address = "5GFAWEKfV6awpZUzAcuPaBjZaHDGoi37BkmjE5mxRcbvkxY1"
roomba_key = "0xe6a576226ab22016c7873f15922e9ec2ff59498260ebdb7b39337214370422c4"
work_address = "5Ci61tCV7GgooiCb8W2jnZFsdSTfURCVpXPXS5JCAdqRGFiQ"
robonomics_path = "/home/alena/"

rospy.init_node('robonomics_listener', anonymous=False)
client = ipfshttpclient.connect()

# Call service send_command
def send_command_client(command):
    rospy.wait_for_service('send_command')
    try:
        send_command = rospy.ServiceProxy('send_command', Command)
        resp = send_command(command)
        return resp
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)

def listener(data):
    if write:
        file.write('\n')
        file.write(str(data))

def clean(duration):
    first_time = time.time()
    send_command_client('Start')
    global file
    file = open('data', 'w')
    global write
    write = True
    while (time.time() - first_time) < duration:
        rospy.Subscriber('/mission', Mission, listener)
    write = False
    print('Work done')
    file.close()
    send_command_client('Stop')
    time.sleep(2)
    send_command_client('Home')
    res = client.add('data')
    print('Data sent to IPFS')
    command = "echo \"Hash: " + res['Hash'] + "\" | " + robonomics_path + "robonomics io write datalog -s " + roomba_key
    send_datalog = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    print('Hash sent to datalog')

if __name__ == "__main__":
    work_paid = True
    proc = robonomics_path + "robonomics io read launch"
    process = subprocess.Popen(proc, shell=True, stdout=subprocess.PIPE)
    #while True:
    if work_paid:
        print("Waiting for payment")
    try:
        output = process.stdout.readline()
        print(output.strip())
        print(work_address + " >> " + roomba_address + " : true")
        if output.strip() == work_address + " >> " + roomba_address + " : true":
            print("Work paid")
            work_paid = True
            clean(5)
        else:
            work_paid = False

    except KeyboardInterrupt:
        exit()
