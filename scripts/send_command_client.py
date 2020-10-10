#!/usr/bin/env python3
import rospy
import json
from std_msgs.msg import String
from roomba980.msg import Mission
from roomba980.srv import Command
import subprocess
import os
import time
import ipfshttpclient
import yaml


class CommandSender:
    def __init__(self):
        rospy.init_node("robonomics_listener", anonymous=False)
        self.file = None
        self.write = False
        config_path = rospy.get_param("~config")

        try:
            with open(config_path) as f:
                content = f.read()
                self.config = yaml.load(content, Loader=yaml.FullLoader)
                rospy.logdebug(f"Configuration dict: {content}")
        except Exception as e:
            while True:
                rospy.logerr("Configuration file is broken or not readable!")
                rospy.logerr(e)
                rospy.sleep(5)

        self.ipfsclient = ipfshttpclient.connect()

    # Call service send_command
    def send_command_client(self, command):
        rospy.wait_for_service('send_command')
        try:
            send_command = rospy.ServiceProxy('send_command', Command)
            resp = send_command(command)
            return resp
        except rospy.ServiceException as e:
            print("Service call failed: %s"%e)

    def listener(self, data):
        if self.write:
            print(1)
            time.sleep(1)
            self.file.write('\n')
            self.file.write(str(data))


    def clean(self, duration):
        dirname = os.path.dirname(__file__)
        print(dirname)
        first_time = time.time()
        self.send_command_client('Start')
        self.file = open(dirname + "/data", 'w')
        self.write = True
        while (time.time() - first_time) < duration:
            #print(2)
            rospy.Subscriber('/roomba/mission', Mission, self.listener)
        self.write = False
        print('Work done')
        time.sleep(1)
        self.file.close()
        self.send_command_client('Stop')
        time.sleep(2)
        self.send_command_client('Home')
        res = self.ipfsclient.add(dirname + "/data")
        os.remove(dirname + "/data")
        print('Data sent to IPFS')
        command = "echo \"Hash: " + res['Hash'] + "\" | " + self.config["path"]["robonomics"] + "robonomics io write datalog -s " + self.config["robonomics"]["roomba_key"]
        send_datalog = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        print('Hash sent to datalog')

    def spin(self):
        work_paid = True
        proc = self.config["path"]["robonomics"] + "robonomics io read launch"
        process = subprocess.Popen(proc, shell=True, stdout=subprocess.PIPE)
        while True:
            #process = subprocess.Popen(proc, shell=True, stdout=subprocess.PIPE)
            if work_paid:
                print("Waiting for payment")
            try:
                output = process.stdout.readline()
                #print(output.strip())
                #print("b\'" + self.config["robonomics"]["work_address"] + " >> " + self.config["robonomics"]["roomba_address"] + " : true" + "\'")
                if str(output.strip()) == "b\'" + self.config["robonomics"]["work_address"] + " >> " + self.config["robonomics"]["roomba_address"] + " : true" + "\'":
                    print("Work paid")
                    work_paid = True
                    self.clean(5)
                else:
                    work_paid = False

            except KeyboardInterrupt:
                exit()
            #process.kill()
        rospy.spin()


if __name__ == "__main__":
    #while True:
    CommandSender().spin()

