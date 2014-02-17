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
tri_hexes=[]
pts_list=[]
slope_right=[]
slope_bottom=[]
slope_left=[]
color_list=['blue','green','red','cyan','magenta','yellow']

def crt2ax(x,y,size):
    q,r = approxAx(x, y, size)
    x,y,z = ax2cb(q,r)
    x,y,z = hexRound(x,y,z)
    return cb2ax(x,y,z)

#npts=7 # number of points
#readdata = np.genfromtxt('/Users/shibikannan/Desktop/SeniorResearch/galaxyhex.csv', delimiter = ',')

# Input parameters

bound = input('bound: ')
x = input('x: ')
y = input('y: ')
radius = input('radius: ')

test_x = x
test_y = y-5

size=1 #in Megaparsecs
n= 2*bound

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

#for index in range(0,6):
#    if (index == 5):    
#        slope_right.append((pts_list[index][1]-y)/(pts_list[0][0]-x))
#        slope_left.append((pts_list[0][1]-y)/(pts_list[index][0]-x))
#        slope_bottom.append((pts_list[0][1]-pts_list[index][1])/(pts_list[0][0]-pts_list[index][0]))
#    else:
#        slope_right.append((pts_list[index][1]-y)/(pts_list[index+1][0]-x))
#        slope_left.append((pts_list[index+1][1]-y)/(pts_list[index][0]-x))
#        slope_bottom.append((pts_list[index+1][1]-pts_list[index][1])/(pts_list[index+1][0]-pts_list[index][0]))
        
for index in range(0,6):
    slope_right.append((pts_list[index][1]-y)/(pts_list[index][0]-x))
    slope_left.append((pts_list[index-1][1]-y)/(pts_list[index-1][0]-x))
    slope_bottom.append((pts_list[index][1]-pts_list[index-1][1])/(pts_list[index][0]-pts_list[index-1][0]))

q_xy,r_xy = crt2ax(test_x,test_y,size)

for r in range(-n,n):
	for q in range(-n,n):
            hex_center = drawConvert(q,r,size)
            if (abs(hex_center[0])<bound+size and abs(hex_center[1])<bound+size and hex_center[0]>=0 and hex_center[1]>=0):
                if (
                        hex_center[1]>=slope_left[0]*(hex_center[0]-x)+y and
                        hex_center[1]<=slope_bottom[0]*(hex_center[0]-pts_list[0][0])+pts_list[0][1] and
                        hex_center[1]>=slope_right[0]*(hex_center[0]-x)+y
                    ):
                        hexes.append([q,r])
                        polygon = mpatches.RegularPolygon(hex_center, 6, size, color='red', ec='black')
                        patches.append(polygon)
                        counter += 1
                        tri_hexes.append([q,r])
                elif (
                        hex_center[1]<=slope_left[1]*(hex_center[0]-x)+y and
                        hex_center[1]<=slope_bottom[1]*(hex_center[0]-pts_list[1][0])+pts_list[1][1] and
                        hex_center[1]>=slope_right[1]*(hex_center[0]-x)+y
                    ):
                        hexes.append([q,r])
                        polygon = mpatches.RegularPolygon(hex_center, 6, size, color='blue', ec='black')
                        patches.append(polygon)
                        counter += 1
                        tri_hexes.append([q,r])
                elif (
                        hex_center[1]<=slope_left[2]*(hex_center[0]-x)+y and
                        hex_center[1]>=slope_bottom[2]*(hex_center[0]-pts_list[2][0])+pts_list[2][1] and
                        hex_center[1]>=slope_right[2]*(hex_center[0]-x)+y
                    ):
                        hexes.append([q,r])
                        polygon = mpatches.RegularPolygon(hex_center, 6, size, color='green', ec='black')
                        patches.append(polygon)
                        counter += 1
                        tri_hexes.append([q,r])
                elif (
                        hex_center[1]<=slope_left[3]*(hex_center[0]-x)+y and
                        hex_center[1]>=slope_bottom[3]*(hex_center[0]-pts_list[3][0])+pts_list[3][1] and
                        hex_center[1]<=slope_right[3]*(hex_center[0]-x)+y
                    ):
                        hexes.append([q,r])
                        polygon = mpatches.RegularPolygon(hex_center, 6, size, color='cyan', ec='black')
                        patches.append(polygon)
                        counter += 1
                        tri_hexes.append([q,r])
                elif (
                        hex_center[1]>=slope_left[4]*(hex_center[0]-x)+y and
                        hex_center[1]>=slope_bottom[4]*(hex_center[0]-pts_list[4][0])+pts_list[4][1] and
                        hex_center[1]<=slope_right[4]*(hex_center[0]-x)+y
                    ):
                        hexes.append([q,r])
                        polygon = mpatches.RegularPolygon(hex_center, 6, size, color='magenta', ec='black')
                        patches.append(polygon)
                        counter += 1
                        tri_hexes.append([q,r])
                elif (
                        hex_center[1]>=slope_left[5]*(hex_center[0]-x)+y and
                        hex_center[1]<=slope_bottom[5]*(hex_center[0]-pts_list[5][0])+pts_list[5][1] and
                        hex_center[1]<=slope_right[5]*(hex_center[0]-x)+y
                    ):
                        hexes.append([q,r])
                        polygon = mpatches.RegularPolygon(hex_center, 6, size, color='yellow', ec='black')
                        patches.append(polygon)
                        counter += 1
                        tri_hexes.append([q,r])                        
                elif (q_xy == q and r_xy == r):
                        hexes.append([q,r])
                        polygon_xy = mpatches.RegularPolygon(hex_center, 6, size, color='black', ec='black')
                        patches.append(polygon_xy)
                else:
                        hexes.append([q,r])
                        polygon2 = mpatches.RegularPolygon(hex_center, 6, size, color='none', ec='black')
                        patches.append(polygon2)
                        counter2 += 1 

#tri_hexes.reverse()
#new_index = tri_hexes
#
#loc_x,loc_y = crt2ax(x,y-9,size)
#output = [new_index.index([loc_x,loc_y])+1,[x,y-9]]
#print output
                     
       
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
