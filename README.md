# roomba980
ROS package to send and recive messages from Roomba980.
Thanks to https://github.com/NickWaterton/Roomba980-Python for python library to communicate with Roomba.
***
## Installation
Install python library to connect with Roomba:
```bash
pip3 install paho-mqtt
pip3 install six
git clone https://github.com/NickWaterton/Roomba980-Python.git
cd Roomba980-Python/roomba
pip3 uninstall enum34
```
Install ROS package into your ROS workspace:
```bash
cd catkin_ws/src
git clone https://github.com/LoSk-p/roomba980
cd ..
catkin_make
```
***
## Configuration
Edit config file in roomba980/src, write your roomba's IP, blid and password. In files send_command_server.py and pub_data.py edit lines 7 and 10 writing your path to python Roomba library and roomba980 ROS package.
***
## Running
You can see roomba' states running getMission node:
```bash
rosrun roomba980 pub_data.py
```
It publish information in mission topic.
Running send_command service you can send roomba some commands:
```bash
rosrun roomba980 send_command_server.py
```
Then call service with 'Start', 'Stop' or 'Home' argument:
```bash
rosservice call /send_command "command: 'Start'"
```

