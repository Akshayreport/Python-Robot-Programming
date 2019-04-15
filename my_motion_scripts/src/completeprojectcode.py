#!/usr/bin/env python

country = 0 
inp = 0
pausest = 0
nonstop = 0
record = 0
samplerate = 0

import sys
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

stopping = 0
print("This program will record the green ball's trajectory as you move it")
print("Then it will move the robot in the exact same way as you moved the ball")
print("The sample rate is the amount of time the program will read the coordinates of the ball")
print("Simple shapes require a larger sampling time of 1 second while complex shapes require a sampling time of 0.5 seconds")
record = (input("Enter the sample rate in seconds then press enter"))

record = record * 20

# For OpenCV2 image display
WINDOW_NAME = 'GreenBallTracker' 
f=open("text", "w")
fy=open("y", "w") # opens text files to store the coordinates of the ball


def track(image):



    stopping = 0
    bobx = 0
    
    blur = cv2.GaussianBlur(image, (5,5),0) # This line will blur the image

    # This will convert the RGB stream to a HSV representation
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # Ensuring the filters for light and dark green
    lower_green = np.array([40,70,70])
    upper_green = np.array([80,200,200])

    # Will make sure that the mask window will only recognise the green colours
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Blur to increase accuracy of the ball
    bmask = cv2.GaussianBlur(mask, (5,5),0)

    # Take the moments to get the centroid
    moments = cv2.moments(bmask)
    m00 = moments['m00']
    centroid_x, centroid_y = None, None
    if m00 != 0:
        centroid_x = int(moments['m10']/m00)
        centroid_y = int(moments['m01']/m00)

  
    ctr = (-1,-1)
    start = 0
    startx = 0	
    global country
    global inp
    global pausest
    global nonstop
    global record
    global samplerate
    if (inp == 0):
	starting = int(input("Start"))
	record = samplerate*20
    	#starting = int(input("Start"))
	inp = 1
   
    
    
    # Use centroid if it exists
    if centroid_x != None and centroid_y != None:

        ctr = (centroid_x, centroid_y)
	startx = float(centroid_x)
	
			
        #print("x =" + str(centroid_x)+ "  y = "+ str(centroid_y))
	bobx = float(centroid_x)
	#print(bobx)
	#print(stopping)
	
        	#f.write("x =" + str(centroid_x)+ "  y = "+ str(centroid_y))
	if inp ==1:
		#print("recorded")
		record = record + 1
		if record == 30:
			record = 0
			print("Recorded")
			f.write(str(centroid_x))
			f.write("\n")
			fy.write(str(centroid_y))
			fy.write("\n")
		
	
		
        	
		
	if bobx > 475  and bobx < 530:
		stopping = 1

       

        # Put black circle at centroid of the green ball
        cv2.circle(image, ctr, 4, (0,0,0))


    # Display full-color image
    cv2.imshow(WINDOW_NAME, image)
    cv2.imshow("HSVfilter", mask)
    if nonstop == 0:
	if pausest == 0:
		rospy.sleep(4)
		nonstop = 1

 
  
    # Force image display, setting centroid to None on ESC key input
    if cv2.waitKey(1) & 0xFF == 27:
        ctr = None
    
    # Return coordinates of centroid
    return ctr

# Test with input from camera
if __name__ == '__main__':

    capture = cv2.VideoCapture(0)
    
   
    while True:

        okay, image = capture.read()

        if okay:

            if not track(image):
                break
          
            if cv2.waitKey(1) & 0xFF == 27:
                break


        else:

           print('Capture failed')
           break


print("The trajectory has been saved")
f.close()
fy.close()

#nextcode = int(input("Press 1 and enter to move robot in a way that it will copy your trajectory"))
f= open("text", "r")
fy= open("y", "r")


moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial', anonymous=True)

robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()    
group = moveit_commander.MoveGroupCommander("manipulator")
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory)
#print group.get_current_pose()
a = float(0.2)
b = float(0.5)
c = float(0.2)
l = 1
#liner = f.readline(1)
#linev = float(liner)
#print linev

xInts = []
for valx in f.read().split():
    xInts.append(float(valx))

yInts = []
for valy in fy.read().split():
    yInts.append(float(valy))

print("Close graph to move on")

plt.plot(xInts, yInts, color='red', marker='x', linestyle='dashed',linewidth=2, markersize=12)
plt.title('trajectory of the ball')
plt.xlabel('x')
plt.ylabel('y')
plt.xlim(0,600)
plt.ylim(0,600)
plt.show()




nextcode = int(input("Press 1 and enter to move robot in a way that it will copy your trajectory"))

sizeofint = len(xInts)



#print theInts[0]

#print theInts[1]



xcoor = map(float,xInts)
ycoor = map(float,yInts)

i = 0
for i in range(sizeofint):
	xcoor[i] = xcoor[i]/1000
	#print(float(lol[i+2]))
p = 0
for p in range(sizeofint):
	
	ycoor[p]= ((ycoor[p]*-1)+500)
	ycoor[p] = ycoor[p]/1000
	#print(float(loly[p]))















#liner = f.readline(2)
#linev = float(liner)

#print linevone
#print linev

#car = f.readline(1)
#car = f.read(3) 
#newx = float(car)

#while l<sizeofint:
l = 0
while l < sizeofint-1:

	
	pose_target = geometry_msgs.msg.Pose()
	pose_target.orientation.w = 1.1
	pose_target.position.x = xcoor[l]
	#pose_target.position.x = 0.35
	pose_target.position.y = 0.6
	pose_target.position.z = ycoor[l]+0.1
	group.set_pose_target(pose_target)
	
	##The lines above will move the robot using the coordinates it received from the ball's motion
	#car = f.readline(1) 
	
	#print f.read(0) 
	

	plan1 = group.plan()
	group.go(wait=True)
	rospy.sleep(3)

	print group.get_current_pose()
	posecheck = group.get_current_pose()
	xpose = posecheck.pose.position.x
	ypose = posecheck.pose.position.z
	checker = xcoor[l]
	
            
	if xpose > checker - 0.1 and xpose < checker +0.1:
		print("coordinates matches")

	else:
		print("Coordinates did not match, Program will stop.")
		sys.exit()


	#liner = f.readline(l+1)
	#linev = float(liner)
	#linev = linev/1000

	pose_target = geometry_msgs.msg.Pose()
	pose_target.orientation.w = 1.1
	pose_target.position.x = xcoor[l+1]
	pose_target.position.y = 0.6
	pose_target.position.z = ycoor[l+1]+0.1
	group.set_pose_target(pose_target)
	plan1 = group.plan()
	group.go(wait=True)
	rospy.sleep(3)

	print group.get_current_pose()
	posecheck = group.get_current_pose()
	xpose = posecheck.pose.position.x
	ypose = posecheck.pose.position.z
	checker = xcoor[l+1]
	
            
	if xpose > checker - 0.1 and xpose < checker +0.1:
		print("coordinates matches")

	else:
		print("Coordinates did not match, Program will stop.")
		sys.exit()

	
      

	#print car
	print group.get_current_pose()
	l = l + 1
	
	
	
	rospy.sleep(0.001)
