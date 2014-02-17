# FOR REGULAR HEXAGON CENTERED AT (35,35) WITH "RADIUS" 20

# LIBRARIES

import random
import numpy as np
from hex_coordinates import *
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
from collections import Counter
import math
import pandas
from matplotlib.patches import Polygon


# HEXAGON GRID SETUP
# Note that we are restricted to the 1st quadrant

counter = 0
counter2 = 0
fig, ax = plt.subplots()
patches = []
hexes=[]
pts_list=[]

def crt2ax(x,y,size):
    q,r = approxAx(x, y, size)
    x,y,z = ax2cb(q,r)
    x,y,z = hexRound(x,y,z)
    return cb2ax(x,y,z)

#npts=7 # number of points
#readdata = np.genfromtxt('/Users/shibikannan/Desktop/SeniorResearch/galaxyhex.csv', delimiter = ',')

# Input parameters

x = input('x: ')
y = input('y: ')
radius = input('radius: ')

test_x = x
test_y = y-5

size=1 #in Megaparsecs
bound=200 # 0 to what in (x,y)
n=250

for k in range(0,6):
    pts_list.append([(x + radius*math.cos((2*math.pi*(k+1))/6)),(y + radius*math.sin((2*math.pi*(k+1))/6))])

for a in range(0,6):
    if (a == 5):
        pts = np.array([[x,y],pts_list[5],pts_list[0]])
        patches.append(Polygon(pts, closed=True,facecolor='none',linewidth=3))
    else:
        pts = np.array([[x,y],pts_list[a],pts_list[a+1]])
        patches.append(Polygon(pts, closed=True,facecolor='none',linewidth=3))
        
print pts_list

slope_right = (pts_list[4][1]-y)/(pts_list[4][0]-x)
slope_left = (pts_list[3][1]-y)/(pts_list[3][0]-x)
lower_bound = pts_list[3][1]
        
q_xy,r_xy = crt2ax(test_x,test_y,size)

for r in range(-n,n):
	for q in range(-n,n):
            hex_center = drawConvert(q,r,size)
            if (abs(hex_center[0])<bound+size and abs(hex_center[1])<bound+size and hex_center[0]>=0 and hex_center[1]>=0):
                if (q_xy == q and r_xy == r):
                    hexes.append([q,r])
                    polygon_xy = mpatches.RegularPolygon(hex_center, 6, size, color='green', ec='black')
                    patches.append(polygon_xy)
                elif (hex_center[1]<=slope_left*(hex_center[0]-x)+y and
                        hex_center[1]>=lower_bound and
                        hex_center[1]<=slope_right*(hex_center[0]-x)+y):
                    hexes.append([q,r])
                    polygon = mpatches.RegularPolygon(hex_center, 6, size, color='blue', ec='black')
                    patches.append(polygon)
                    counter += 1
                else:
                    hexes.append([q,r])
                    polygon2 = mpatches.RegularPolygon(hex_center, 6, size, color='none', ec='black')
                    patches.append(polygon2)
                    counter2 += 1
                
plt.axes().set_aspect('equal', 'datalim')
    
collection = PatchCollection(patches, cmap=plt.cm.hsv, alpha=0.3, match_original=True)
ax.add_collection(collection)
plt.axis([-10,bound+5,-10,bound+5])
plt.show()

print 'hex in wedge ',counter
print 'hex not in wedge ',counter2
print '(x,y) = ',x,y
print '(q,r) = ',q_xy,r_xy

#n_gal= 5
#for i in range(len(hexes)):
#    if hex_counts[i]>n_gal:
#        hex_counts[i]=n_gal
#        
#        
#printlist = []
#for i in range(len(hexes)):
#    if hex_counts[i] > 0:
#        printlist.append([hexes[i],hex_counts[i]])
#
#histdata = Counter(hex_counts)
#print histdata.most_common()
#print printlist, sum(hex_counts)
##plt.hist(hex_counts,bins=[1,2,3,4,5,6])
##plt.show()
