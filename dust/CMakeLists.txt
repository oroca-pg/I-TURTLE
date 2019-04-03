cmake_minimum_required(VERSION 2.8.3)
project(dust)

find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  message_generation
)

catkin_python_setup()

add_service_files(
  FILES
  dust.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES dust
  CATKIN_DEPENDS rospy std_msgs message_runtime
#  DEPENDS system_lib
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

install(PROGRAMS
  scripts/server
  scripts/client
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}/scripts
)

