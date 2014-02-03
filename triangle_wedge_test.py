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
n=100
hexes=[]

def crt2ax(x,y,size):
    q,r = approxAx(x, y, size)
    x,y,z = ax2cb(q,r)
    x,y,z = hexRound(x,y,z)
    return cb2ax(x,y,z)

#npts=7 # number of points
#readdata = np.genfromtxt('/Users/shibikannan/Desktop/SeniorResearch/galaxyhex.csv', delimiter = ',')

# Input parameters
size=1 #in Megaparsecs
bound=60 # 0 to what in (x,y)
x = 35
y = 30


q_xy,r_xy = crt2ax(x,y,size)

for r in range(-n,n):
	for q in range(-n,n):
            hex_center = drawConvert(q,r,size)
            if (abs(hex_center[0])<bound+size and abs(hex_center[1])<bound+size and hex_center[0]>=0 and hex_center[1]>=0):
                if (q_xy == q and r_xy == r):
                    hexes.append([q,r])
                    polygon_xy = mpatches.RegularPolygon(hex_center, 6, size, color='green', ec='black')
                    patches.append(polygon_xy)
                elif (hex_center[1]<=95.62-1.732*hex_center[0] and hex_center[1] >= 17.68 and hex_center[1]<=1.732*hex_center[0]-25.62):
                    hexes.append([q,r])
                    polygon = mpatches.RegularPolygon(hex_center, 6, size, color='blue', ec='black')
                    patches.append(polygon)
                    counter += 1
                else:
                    hexes.append([q,r])
                    polygon2 = mpatches.RegularPolygon(hex_center, 6, size, color='none', ec='black')
                    patches.append(polygon2)
                    counter2 += 1

                
pts1 = np.array([[35,35],[25,17.68],[45,17.68]])
pts2 = np.array([[35,35],[55,35],[45,17.68]])
pts3 = np.array([[35,35],[55,35],[45,52.32]])
pts4 = np.array([[35,35],[45,52.32],[25,52.32]])
pts5 = np.array([[35,35],[25,52.32],[15,35]])
pts6 = np.array([[35,35],[25,17.68],[15,35]])

p1 = Polygon(pts1, closed=True,facecolor='none',linewidth=3)
p2 = Polygon(pts2, closed=True,facecolor='none',linewidth=3)
p3 = Polygon(pts3, closed=True,facecolor='none',linewidth=3)
p4 = Polygon(pts4, closed=True,facecolor='none',linewidth=3)
p5 = Polygon(pts5, closed=True,facecolor='none',linewidth=3)
p6 = Polygon(pts6, closed=True,facecolor='none',linewidth=3)

patches.append(p1)
patches.append(p2)
patches.append(p3)
patches.append(p4)
patches.append(p5)
patches.append(p6)

plt.axes().set_aspect('equal', 'datalim')

#
## Reading CSV
#k = [] # x in file
#l = [] # y in file
#
#color=['go']*npts
##hexes = [0]*npts
#hex_counts = [0]*(len(hexes)+1)
#
#for i in range(1,npts):
#    k.append(readdata[i][4])
#    l.append(readdata[i][5])
#    
#
#for i in range(1,npts-1):
#    x = k[i]
#    y = l[i]
#    q,r = crt2ax(x,y,size)
#    #hexes[i] = [q,r]
#    try:
#        index = hexes.index([q,r])
#    except:
#        index = len(hexes)
#    hex_counts[index] += 1
#    plt.plot(x,y,color[i])
    
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
