import random
import numpy as np
from hex_coordinates import *
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection

# setting up initial field of hexagons
fig, ax = plt.subplots()
patches = []
size=5
n=20
bound=20
hexes=[]
for r in range(-n,n+1):
	for q in range(-n,n):
            hex_center = drawConvert(q,r,size)
            if (abs(hex_center[0])<bound and abs(hex_center[1])<bound):
                hexes.append([q,r])
                polygon = mpatches.RegularPolygon(hex_center, 6, size, fill=False)
                patches.append(polygon)

def crt2ax(x,y,s):
    q,r = approxAx(x, y, s)
    x,y,z = ax2cb(q,r)
    x,y,z = hexRound(x,y,z)
    return cb2ax(x,y,z)

# hexagon/point test
npts=100
color=['go']*npts
#hexes = [0]*npts
hex_counts = [0]*(len(hexes)+1)

for i in range(npts):
    x = random.uniform(-bound,bound)
    y = random.uniform(-bound,bound)
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
plt.axis('equal')
plt.plot(0,0,'b*')
plt.show()

n_gal=3
for i in range(len(hexes)):
    if hex_counts[i]>n_gal:
        hex_counts[i]=n_gal
        
print hex_counts, sum(hex_counts)
