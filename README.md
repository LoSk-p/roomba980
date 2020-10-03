# roomba980
ROS package to send and recive messages from Roomba980.
Thanks to https://github.com/NickWaterton/Roomba980-Python for python library to communicate with Roomba.
***
## Requirements
* ROS melodic (installation instraction [here](http://wiki.ros.org/melodic/Installation/Ubuntu))
* IPFS 0.4.22 (download from [here](https://www.npackd.org/p/ipfs/0.4.22) and install)
```bash
tar -xvzf go-ipfs_v0.4.22_linux-386.tar.gz
cd go-ipfs/
sudo bash install.sh
ipfs init
```
* ipfshttpclient
```bash
pip install ipfshttpclient
```
* Robonomics node (binary file) (download latest release [here](https://github.com/airalab/robonomics/releases))
***
## Installation
Install python library:
```bash
pip3 install paho-mqtt
pip3 install six
git clone https://github.com/NickWaterton/Roomba980-Python.git
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
Edit config.yaml file in roomba980/src. In "path" write your path to robonomics file and to Roomba980-Python directory
***
## Running
### Running robonomics
Go to the folder with robonomics file and create a local robonomics network:
```bash
./robonomics --dev --rpc-cors all
```

![robonomics](https://github.com/LoSk-p/media/blob/master/2.png)

Go to https://parachain.robonomics.network and switch to local node

![local](https://github.com/LoSk-p/media/blob/master/3.png)

Then go to Accounts and create ROOMBA and WORK accounts. Save account's names and keys, you will need them later

![acc](https://github.com/LoSk-p/media/blob/master/4.png)

![accs](https://github.com/LoSk-p/media/blob/master/Screenshot%20from%202020-09-18%2001-07-56.png)
***
### Running ipfs
Run ipfs daemon:
```bash
ipfs daemon
```
### Running Roomba package
You can see roomba's states running getMission node:
```bash
rosrun roomba980 pub_data.py
```
It publish information in mission topic.
Then run send_data_client.py
```bash
python send_data_client.py
```
And send the transaction
```bash
echo "ON" | ./robonomics io write launch -r <ROOMBA_ADDRESS> -s <WORK_KEY>
```
Where <ROOMBA_ADDRESS> and <WORK_KEY> are address and key from your accounts.
Your Roomba will start cleaning and will return to charge after 10 minutes.


