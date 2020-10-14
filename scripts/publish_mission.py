#!/usr/bin/env python3
import rospy
import json
import time
from std_msgs.msg import String
from roomba980.msg import Mission
from roomba980.srv import Command
import sys
import os
import yaml
from roomba import Roomba


class PublishMission:
    def __init__(self):
        rospy.init_node("mission_publisher", anonymous=True)

        config_path = rospy.get_param("~config")

        try:
            with open(config_path) as f:
                content = f.read()
                config = yaml.load(content, Loader=yaml.FullLoader)
                rospy.logdebug(f"Configuration dict: {content}")
        except Exception as e:
            while True:
                rospy.logerr("Configuration file is broken or not readable!")
                rospy.logerr(e)
                rospy.sleep(5)

        self.myroomba = Roomba(config["roomba"]["IP"], config["roomba"]["blid"], config["roomba"]["password"])
        self.myroomba.connect()
        time.sleep(5)
        while not self.myroomba.roomba_connected:
            #print(1)
            time.sleep(1)
        print("Roomba connected")
        rospy.Service("send_command", Command, self.send_command)
        self.pub_mission = rospy.Publisher("mission", Mission, queue_size=10)

    def send_command(self, req):
        if req.command == "Start":
            self.myroomba.send_command("start")
            return("Starting cleaning")
        elif req.command == "Stop":
            self.myroomba.send_command("stop")
            return("Stop cleaning")
        elif req.command == "Home":
            self.myroomba.send_command("dock")
            return("Going back home")
        else:
            return("Wrong command")

    def get_msg_data(self, data, data_state, data_error):
        miss_msg = Mission()
        miss_msg.name = data["name"]
        miss_msg.batteryPercentage = str(data["batPct"])
        miss_msg.mission_cycle = data["cleanMissionStatus"]["cycle"]
        miss_msg.mission_phase = data["cleanMissionStatus"]["phase"]
        miss_msg.current_state = data_state
        miss_msg.error = data_error
        miss_msg.mission_notReady = str(data["cleanMissionStatus"]["notReady"])
        miss_msg.robotPositionXY[0] = data["pose"]["point"]["x"]
        miss_msg.robotPositionXY[1] = data["pose"]["point"]["y"]
        miss_msg.robotPositionAngle = data["pose"]["theta"]
        miss_msg.audio = str(data["audio"]["active"])
        return(miss_msg)

    def spin(self):
        rate = rospy.Rate(1)
        while not rospy.is_shutdown():
            #data = {"name": "robot", "batPct": 100, "cleanMissionStatus": {"cycle": "none", "phase": "charge", "error": 0, "notReady": 0}, "pose": {"point": {"x": 100, "y": 20},"theta": -28}, "audio": {"active": True}}
            #data_state = "Charging"
            data_state = self.myroomba.current_state
            data1 = self.myroomba.master_state
            data_error = self.myroomba.error_message
            data = data1["state"]["reported"]
            mission_msg = self.get_msg_data(data, data_state, data_error)
            self.pub_mission.publish(mission_msg)
            rate.sleep()


if __name__ == "__main__":
    PublishMission().spin()

