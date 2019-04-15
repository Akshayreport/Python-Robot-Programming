import sys
import time
import cv2
import numpy as np


import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg

country = 0 
inp = 0
pausest = 0
nonstop = 0
record = 0
samplerate = 0

stopping = 0
print("This program will record the green ball's trajectory as you move it")
print("Then it will move the robot in the exact same way as you moved the ball")
print("The sample rate is the amount of time the program will read the coordinates of the ball")
print("Simple shapes require a larger sampling time of 1 second while complex shapes require a sampling time of 0.5 seconds")




# For OpenCV2 image display
WINDOW_NAME = 'GreenBallTracker' 
f=open("text", "w")
fy=open("y", "w")


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
    global record
    global pausest
    global nonstop
    global samplerate
    #global record
    if (inp == 0):
	samplerate = (input("Enter the sample rate in seconds then press enter"))
    	starting = int(input("Start"))
	record = samplerate*2
	inp = 1
   
    
    
    #rospy.sleep(0.25)
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

       

        # Put black circle in at centroid in image
        cv2.circle(image, ctr, 4, (0,0,0))


    # Display full-color image
    cv2.imshow(WINDOW_NAME, image)
    cv2.imshow("HSVFilter", mask)
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
