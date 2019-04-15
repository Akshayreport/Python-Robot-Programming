import matplotlib.pyplot as plt

#This program draws a trajectory mapping graph of the ball in motion

f= open("text", "r")
fy= open("y", "r")

xInts = []
for valx in f.read().split():
    xInts.append(float(valx))

yInts = []
for valy in fy.read().split():
    yInts.append(float(valy))

plt.plot(xInts, yInts, color='red', marker='x', linestyle='dashed',linewidth=2, markersize=12)
plt.title('trajectory of the ball')
plt.xlabel('x')
plt.ylabel('y')
plt.xlim(0,600)
plt.ylim(0,600)
plt.show()
##Creates a dashed lines between the points which will illustrate the ball's trajectory
