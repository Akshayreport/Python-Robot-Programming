READ ME FILE


Please download the necessary files below before compiling the codes :

Ubuntu 16.04: Follow the instructions at http://releases.ubuntu.com/16.04/

Python 3.6: Follow the instructions at http://ubuntuhandbook.org/index.php/2017/07/install-python-3-6-1-in-ubuntu-16-04-lts/

OpenCV : Follow the instructions at https://www.learnopencv.com/install-opencv-3-4-4-on-ubuntu-16-04/

ROS Kinetic: Follow the instructions at   http://wiki.ros.org/kinetic/Installation/Ubuntu

Move-it: Follow the instructions at https://moveit.ros.org/install/

UR5 Collaborative robot arm: Download the entire file at https://github.com/ros-industrial/universal_robot

Please make sure that the UR5 file is saved inside the catkin source folder which will be created after ROS has been downloaded.

Please save the files that I uploaded into the catkin source folder.



Once the files have been saved and downloaded into the correct directory, the program will be ready 
to launch as the configuration has already been made in my uploaded files.


1) Open 3 terminal files

2)Please launch in a seperate terminal : roslaunch ur_gazebo ur5.launch	
3)Please launch in a seperate terminal : roslaunch demo_moveit_config demo_planning_execution.launch 
4)Please launch in a seperate terminal : rosrun my_motion_scripts completeprojectcode.py 

The program will begin. Please follow the instructions clearly.

Overview of program: User will be instructed to move a green ball, press 1 to record and Escape to stop recording. 
The UR5 will replicate the ball's trajectory