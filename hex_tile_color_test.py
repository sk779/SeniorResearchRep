import math, random
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection

# using a pointy-top hexagon arrangement

# estimate axial coordinates based on x, y
def approxAx(x,y,s):
	q = ((math.sqrt(3.)/3.)*x-y/3.)/s
	r = (2./3.)*(y/s)
	return q, r

# convert from axial to cube coordinates
def ax2cb(q,r):
	x = q
	z = r
	y = -x-z
	return x, y, z

# determine the hexagon index based on cube coordinates
def hexRound(x,y,z):
	rx = round(x)
	ry = round(y)
	rz = round(z)
	if (rx+ry+rz)==0:
		return int(rx), int(ry), int(rz)
	else:
		x_err = math.fabs(rx-x)
		y_err = math.fabs(ry-y)
		z_err = math.fabs(rz-z)
		if x_err>y_err and x_err>z_err:
			rx = -ry-rz
		elif y_err>z_err:
			ry = -rx-rz
		else:
			rz = -rx-ry
		return int(rx), int(ry), int(rz)

# convert from cube to axial coordinates
def cb2ax(x,y,z):
	q  =  x
	r = z
	return q, r

# convert from axial to x-y coordinates
def drawConvert(q,r,s):
	x = s * math.sqrt(3) * (q + .5*r)
	y = s * (3./2.) * r
	return [x,y]

def crt2ax(x,y):
    q,r = approxAx(x, y, size)
    x,y,z = ax2cb(q,r)
    x,y,z = hexRound(x,y,z)
    return cb2ax(x,y,z)

# setting up initial field of hexagons
fig, ax = plt.subplots()
patches = []
size=5
n=20
bound=8
for r in range(-n,n+1):
	for q in range(-n,n):
            hex_center = drawConvert(q,r,size)
            if (abs(hex_center[0])<bound and abs(hex_center[1])<bound):
                polygon = mpatches.RegularPolygon(hex_center, 6, size, fill=False)
                patches.append(polygon)


# hexagon/point test
npts=300
#m_x=[random.uniform(-bound,bound) for m in range(npts)]
#m_y=[random.uniform(-bound,bound) for m in range(npts)]
color=['g^']*npts
colors = ['red', 'blue', 'magenta', 'yellow', 'cyan']
colors2 = ['ro', 'bo', 'mo', 'yo', 'co']
hexes = [[0,0], [0,-1], [0,1], [1,-1], [-1,1]]
for i in range(npts):
    x = random.uniform(-bound,bound)
    y = random.uniform(-bound,bound)
    q,r = crt2ax(x,y)
    for j in range(5):
        if [q,r] == hexes[j]:
            color[i] = colors2[j]
    plt.plot(x,y,color[i])
    
#plt.plot(m_x,m_y,color)

#	hex_center = drawConvert(q,r,size)
#	polygon=mpatches.RegularPolygon(hex_center, 6, size, fill=False, color=colors[i], lw=2)
#	patches.append(polygon)

collection = PatchCollection(patches, cmap=plt.cm.hsv, alpha=0.3, match_original=True)
ax.add_collection(collection)
plt.axis('equal')
plt.plot(0,0,'b*')
plt.show()