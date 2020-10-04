cmake_minimum_required(VERSION 2.8.3)
project(roomba980)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  message_generation
)

catkin_python_setup()

## Generate messages in the 'msg' folder
 add_message_files(
   FILES
   Mission.msg
 )

## Generate services in the 'srv' folder
 add_service_files(
   FILES
   Command.srv
 )


## Generate added messages and services with any dependencies listed here
 generate_messages(
   DEPENDENCIES
   std_msgs
 )

catkin_package(
  INCLUDE_DIRS
  LIBRARIES
  CATKIN_DEPENDS message_runtime roscpp rospy std_msgs
  DEPENDS
)

###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

#############
## Install ##
#############

## Mark other files for installation (e.g. launch and bag files, etc.)

catkin_install_python(
    PROGRAMS
        scripts/publish_mission.py
        scripts/send_command_client.py
    DESTINATION
        ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(
	FILES
		launch/robonomics.launch
	DESTINATION
		${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
)

install(
    FILES
        config/config.yaml
    DESTINATION
        ${CATKIN_PACKAGE_SHARE_DESTINATION}/config
)

