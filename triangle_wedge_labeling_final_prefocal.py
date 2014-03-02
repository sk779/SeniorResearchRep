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
x_prime = []
y_prime = []
hex_list = []
error_pts = []

# Cartesian -> Axial

def crt2ax(x,y,size):
    q,r = approxAx(x, y, size)
    x,y,z = ax2cb(q,r)
    x,y,z = hexRound(x,y,z)
    return cb2ax(x,y,z)

# Input

print 'To get ~5000 Hex, radius must be 70 or 71'

bound = 500#input('bound: ')
x = 200#input('x center: ')
y = 300#input('y center: ')
radius = 60#input('radius: ')
pt_num = 1000#input('# rand pts to test: ')

n= 2*bound

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

for i in range(0,6):
    if (i < 2):
        slope_right.append((pts_list[i+4][1]-y)/(pts_list[i+4][0]-x))
        slope_left.append((pts_list[i+3][1]-y)/(pts_list[i+3][0]-x))
        slope_bottom.append((pts_list[i+4][1]-pts_list[i+3][1])/(pts_list[i+4][0]-pts_list[i+3][0]))
    elif (i == 2):
        slope_right.append((pts_list[0][1]-y)/(pts_list[0][0]-x))
        slope_left.append((pts_list[5][1]-y)/(pts_list[5][0]-x))
        slope_bottom.append((pts_list[0][1]-pts_list[5][1])/(pts_list[0][0]-pts_list[5][0]))
    else:
        slope_right.append((pts_list[i-2][1]-y)/(pts_list[i-2][0]-x))
        slope_left.append((pts_list[i-3][1]-y)/(pts_list[i-3][0]-x))
        slope_bottom.append((pts_list[i-2][1]-pts_list[i-3][1])/(pts_list[i-2][0]-pts_list[i-3][0]))

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
                if (hex_center[1]<=slope_left[0]*(hex_center[0]-x)+y and
                        hex_center[1]>=slope_bottom[0]*(hex_center[0]-pts_list[3][0])+pts_list[3][1] and
                        hex_center[1]<=slope_right[0]*(hex_center[0]-x)+y):
                    hexes.append([q,r])
                    tri_hexes.append([q,r])
                    tri_hexes2.append([q,r])
                    polygon = mpatches.RegularPolygon(hex_center, 6, size, color='blue', ec='black')
                    patches.append(polygon)
                    counter += 1
                if (hex_center[1]>=slope_left[1]*(hex_center[0]-x)+y and
                        hex_center[1]>=slope_bottom[1]*(hex_center[0]-pts_list[4][0])+pts_list[4][1] and
                        hex_center[1]<=slope_right[1]*(hex_center[0]-x)+y):
                    hexes.append([q,r])
                    tri_hexes.append([q,r])
#                    tri_hexes2.append([q,r])
                    polygon = mpatches.RegularPolygon(hex_center, 6, size, color='green', ec='black')
                    patches.append(polygon)
                    counter += 1
                if (hex_center[1]>=slope_left[2]*(hex_center[0]-x)+y and
                        hex_center[1]<=slope_bottom[2]*(hex_center[0]-pts_list[5][0])+pts_list[5][1] and
                        hex_center[1]<=slope_right[2]*(hex_center[0]-x)+y):
                    hexes.append([q,r])
                    tri_hexes.append([q,r])
#                    tri_hexes2.append([q,r])
                    polygon = mpatches.RegularPolygon(hex_center, 6, size, color='red', ec='black')
                    patches.append(polygon)
                    counter += 1
                if (hex_center[1]>=slope_left[3]*(hex_center[0]-x)+y and
                        hex_center[1]<=slope_bottom[3]*(hex_center[0]-pts_list[0][0])+pts_list[0][1] and
                        hex_center[1]>=slope_right[3]*(hex_center[0]-x)+y):
                    hexes.append([q,r])
                    tri_hexes.append([q,r])
#                    tri_hexes2.append([q,r])
                    polygon = mpatches.RegularPolygon(hex_center, 6, size, color='cyan', ec='black')
                    patches.append(polygon)
                    counter += 1
                if (hex_center[1]<=slope_left[4]*(hex_center[0]-x)+y and
                        hex_center[1]<=slope_bottom[4]*(hex_center[0]-pts_list[1][0])+pts_list[1][1] and
                        hex_center[1]>=slope_right[4]*(hex_center[0]-x)+y):
                    hexes.append([q,r])
                    tri_hexes.append([q,r])
#                    tri_hexes2.append([q,r])
                    polygon = mpatches.RegularPolygon(hex_center, 6, size, color='magenta', ec='black')
                    patches.append(polygon)
                    counter += 1
                if (hex_center[1]<=slope_left[5]*(hex_center[0]-x)+y and
                        hex_center[1]>=slope_bottom[5]*(hex_center[0]-pts_list[2][0])+pts_list[2][1] and
                        hex_center[1]>=slope_right[5]*(hex_center[0]-x)+y):
                    hexes.append([q,r])
                    tri_hexes.append([q,r])
#                    tri_hexes2.append([q,r])
                    polygon = mpatches.RegularPolygon(hex_center, 6, size, color='yellow', ec='black')
                    patches.append(polygon)
                    counter += 1

                # Tile remaining hexagonal grid (blank)
#                else:
#                        hexes.append([q,r])
#                        polygon2 = mpatches.RegularPolygon(hex_center, 6, size, color='none', ec='black')
#                        patches.append(polygon2)
#                        counter2 += 1

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
#        polygon2 = mpatches.RegularPolygon(hex_center, 6, size, color=color_list[index], ec='black')
#        patches.append(polygon2)
        if (hex_center[1]<=slope_left[0]*(hex_center[0]-x)+y and
                hex_center[1]>=slope_bottom[0]*(hex_center[0]-pts_list[4][0])+pts_list[4][1] and hex_center[1]<=slope_right[0]*(hex_center[0]-x)+y):
            final = [q,r]
            if (index == 0):
                hex_number = index
            elif (y_prime <= y):
                hex_number = -index+6
            else:
                hex_number = index
            #print final, hex_number
            #print g,h
            plt.plot(g, h, 'ro')
    return final, hex_number

# Random Number Generator

for i in range(0,pt_num):
    x_prime.append(random.uniform(2, bound-2))
    y_prime.append(random.uniform(2, bound-2))

plt.plot(x_prime, y_prime, 'bo')
tri_hexes2.reverse()
new_index = tri_hexes2

# Determine Focal Coordinates

i_loop = 0
final_countdown = 0
while (i_loop < len(x_prime)):
    try:
        tri_index = new_index.index(focal_coord(x_prime[i_loop], y_prime[i_loop])[0])+1
        hex_number = focal_coord(x_prime[i_loop], y_prime[i_loop])[1]+1
        hex_list.append(hex_number)
        output = [[x_prime[i_loop],y_prime[i_loop]],tri_index,hex_number]
        i_loop = i_loop + 1
        final_countdown = final_countdown + 1
        # print output
    except (ValueError):
        i_loop = i_loop + 1
        continue

#for i in range(0,len(x_prime)):
#    tri_index = new_index.index(focal_coord(x_prime[i], y_prime[i])[0])+1
#    hex_number = focal_coord(x_prime[i], y_prime[i])[1]+1
#    output = [[x_prime[i],y_prime[i]],tri_index,hex_number]
#    print output

print 'hex in wedge ',counter
print 'hex not in wedge ',counter2
print 'captured points', final_countdown
print Counter(hex_list)

plt.axes().set_aspect('equal', 'datalim')
collection = PatchCollection(patches, cmap=plt.cm.hsv, alpha=0.3, match_original=True)
ax.add_collection(collection)
plt.axis([-10,bound+5,-10,bound+5])
plt.show()

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
