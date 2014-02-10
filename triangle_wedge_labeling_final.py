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

# Global Variables/Initializations

counter = 0
counter2 = 0
fig, ax = plt.subplots()
patches = []
hexes=[]
tri_hexes=[]
tri_hexes2=[]
pts_list=[]
slope_right=[]
slope_bottom=[]
slope_left=[]
color_list=['black','green','red','cyan','magenta','yellow']
size=1

# Cartesian -> Axial

def crt2ax(x,y,size):
    q,r = approxAx(x, y, size)
    x,y,z = ax2cb(q,r)
    x,y,z = hexRound(x,y,z)
    return cb2ax(x,y,z)

# Input

bound = input('bound: ')
x = input('x: ')
y = input('y: ')
radius = input('radius: ')
x_prime_input = input('x prime: ')
y_prime_input = input('y prime: ')

n= 2*bound

#bound = 50
#x = 20
#y = 20
#radius = 10
#test_x = x
#test_y = y-5

# Determine hexagon vertices

for k in range(0,6):
    pts_list.append([(x + radius*math.cos((2*math.pi*(k+1))/6)),(y + radius*math.sin((2*math.pi*(k+1))/6))])

# Draw focal plane

for a in range(0,6):
    if (a == 5):
        pts = np.array([[x,y],pts_list[5],pts_list[0]])
        patches.append(Polygon(pts, closed=True,facecolor='none',linewidth=3))
    else:
        pts = np.array([[x,y],pts_list[a],pts_list[a+1]])
        patches.append(Polygon(pts, closed=True,facecolor='none',linewidth=3))
        
# Slopes of reference triangle (bottom)
        
slope_right = (pts_list[4][1]-y)/(pts_list[4][0]-x)
slope_left = (pts_list[3][1]-y)/(pts_list[3][0]-x)
lower_bound = pts_list[3][1]
        
#q_xy,r_xy = crt2ax(test_x,test_y,size)

# Hexagonal Grid Drawing

for r in range(-n,n):
	for q in range(-n,n):
            hex_center = drawConvert(q,r,size)
            if (abs(hex_center[0])<bound+size and abs(hex_center[1])<bound+size and hex_center[0]>=0 and hex_center[1]>=0):     
                   
                # Axial coordinate check
                #if (q_xy == q and r_xy == r):
                #        hexes.append([q,r])
                #        polygon_xy = mpatches.RegularPolygon(hex_center, 6, size, color='green', ec='black')
                #        patches.append(polygon_xy)
                
                # Tile reference triangle with hexagonal grid (blue)
                if (hex_center[1]<=slope_left*(hex_center[0]-x)+y and
                        hex_center[1]>=lower_bound and
                        hex_center[1]<=slope_right*(hex_center[0]-x)+y):
                        hexes.append([q,r])
                        tri_hexes.append([q,r])
                        tri_hexes2.append([q,r])
                        polygon = mpatches.RegularPolygon(hex_center, 6, size, color='blue', ec='black')
                        patches.append(polygon)
                        counter += 1    
                # Tile remaining hexagonal grid (blank)                                             
                else:
                        hexes.append([q,r])
                        polygon2 = mpatches.RegularPolygon(hex_center, 6, size, color='none', ec='black')
                        patches.append(polygon2)
                        counter2 += 1

# Determining focal plane coordinate scheme
                                                
def focal_coord(x_prime, y_prime):
    final = 0
    hex_number = 0
    for index in range(0,6):
        new_radius = math.sqrt((y_prime-y)*(y_prime-y)+(x_prime-x)*(x_prime-x))
        if (y_prime <= y):
            g = x + new_radius*math.cos(((math.pi/3)*index)-math.acos((x_prime-x)/new_radius))
            h = y + new_radius*math.sin(((math.pi/3)*index)-math.acos((x_prime-x)/new_radius))
        else:
            g = x + new_radius*math.cos(((math.pi/3)*index)-math.acos((x_prime-x)/new_radius))
            h = y - new_radius*math.sin(((math.pi/3)*index)-math.acos((x_prime-x)/new_radius))    
        q,r = crt2ax(g,h,size)
        hex_center = drawConvert(q,r,size)
        polygon2 = mpatches.RegularPolygon(hex_center, 6, size, color=color_list[index], ec='black')
        patches.append(polygon2)
        if (hex_center[1]<=slope_left*(hex_center[0]-x)+y and
            hex_center[1]>=lower_bound and
            hex_center[1]<=slope_right*(hex_center[0]-x)+y):
            final = [q,r]
            if (index == 0):
                hex_number = index
            elif (y_prime <= y):
                hex_number = -index+6
            else:
                hex_number = index
    return final, hex_number

# Output focal plane coordinates

x_prime = [x_prime_input]
y_prime = [y_prime_input]
tri_hexes2.reverse()
new_index = tri_hexes2

for i in range(0,len(x_prime)):
    tri_index = new_index.index(focal_coord(x_prime[i], y_prime[i])[0])+1
    hex_number = focal_coord(x_prime[i], y_prime[i])[1]+1
    output = [[x_prime[i],y_prime[i]],tri_index,hex_number]
    print 'Original Point,Hex #,Triangle #', output

# Drawing                    
       
plt.axes().set_aspect('equal', 'datalim')
collection = PatchCollection(patches, cmap=plt.cm.hsv, alpha=0.3, match_original=True)
ax.add_collection(collection)
plt.axis([-10,bound+5,-10,bound+5])
plt.show()


#print 'hex in wedge ',counter
#print 'hex not in wedge ',counter2
#print '(x,y) = ',x,y
#print '(q,r) = ',q_xy,r_xy
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
