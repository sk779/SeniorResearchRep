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

# HEXAGON GRID SETUP
# Note that we are restricted to the 1st quadrant

# Input parameters
size=100 #in Megaparsecs
npts=7 # number of points
readdata = np.genfromtxt('/Users/shibikannan/Desktop/SeniorResearch/galaxyhex.csv', delimiter = ',')

fig, ax = plt.subplots()
patches = []
n=1000
bound=1000
hexes=[]
for r in range(-n,n):
	for q in range(-n,n):
            hex_center = drawConvert(q,r,size)
            if (abs(hex_center[0])<bound+size and abs(hex_center[1])<bound+size and hex_center[0]>=0 and hex_center[1]>=0):
                hexes.append([q,r])
                polygon = mpatches.RegularPolygon(hex_center, 6, size, fill=False)
                patches.append(polygon)

def crt2ax(x,y,s):
    q,r = approxAx(x, y, s)
    x,y,z = ax2cb(q,r)
    x,y,z = hexRound(x,y,z)
    return cb2ax(x,y,z)

# Reading CSV
k = [] # x in file
l = [] # y in file

color=['go']*npts
#hexes = [0]*npts
hex_counts = [0]*(len(hexes)+1)

for i in range(1,npts):
    k.append(readdata[i][4])
    l.append(readdata[i][5])
    

for i in range(1,npts-1):
    x = k[i]
    y = l[i]
    q,r = crt2ax(x,y,size)
    #hexes[i] = [q,r]
    try:
        index = hexes.index([q,r])
    except:
        index = len(hexes)
    hex_counts[index] += 1
    plt.plot(x,y,color[i])
    
collection = PatchCollection(patches, cmap=plt.cm.hsv, alpha=0.3, match_original=True)
ax.add_collection(collection)
plt.axis([0,1000,0,1000])
plt.plot(0,0,'b*')
plt.show()

n_gal= 5
for i in range(len(hexes)):
    if hex_counts[i]>n_gal:
        hex_counts[i]=n_gal
        
        
printlist = []
for i in range(len(hexes)):
    if hex_counts[i] > 0:
        printlist.append([hexes[i],hex_counts[i]])

histdata = Counter(hex_counts)
print histdata.most_common()
print printlist, sum(hex_counts)
#plt.hist(hex_counts,bins=[1,2,3,4,5,6])
#plt.show()
