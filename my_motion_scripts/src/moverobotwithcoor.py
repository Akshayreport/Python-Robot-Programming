import sys



import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg







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
	#Move the robot depending on the ball's motion
	
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

print("Close graph to move on")

plt.plot(xInts, yInts, color='red', marker='x', linestyle='dashed',linewidth=2, markersize=12)
plt.title('trajectory of the ball')
plt.xlabel('x')
plt.ylabel('y')
plt.xlim(0,600)
plt.ylim(0,600)
plt.show()



