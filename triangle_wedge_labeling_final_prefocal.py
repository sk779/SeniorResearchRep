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
from operator import itemgetter, attrgetter

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
tri1 = []
tri2 = []
tri3 = []
tri4 = []
tri5 = []
tri6 = []


# Cartesian -> Axial

def crt2ax(x,y,size):
    q,r = approxAx(x, y, size)
    x,y,z = ax2cb(q,r)
    x,y,z = hexRound(x,y,z)
    return cb2ax(x,y,z)

# Input

print 'To get ~5000 Hex, radius must be 70 or 71'

bound = input('bound: ')
x = input('x center: ')
y = input('y center: ')
radius = input('radius: ')
pt_num = input('# rand pts to test: ')

#bound = 50
#x = 25
#y = 25
#radius = 10
#pt_num = 10

n= 2*bound

# Determine hexagon vertices

for k in range(0,6):
    pts_list.append([(x + radius*math.cos((2*math.pi*(k+1))/6)),(y + radius*math.sin((2*math.pi*(k+1))/6))])

# Draw focal plane

#for a in range(0,6):
#    if (a == 5):
#        pts = np.array([[x,y],pts_list[5],pts_list[0]])
#        patches.append(Polygon(pts, closed=True,facecolor='none',linewidth=3))
#    else:
#        pts = np.array([[x,y],pts_list[a],pts_list[a+1]])
#        patches.append(Polygon(pts, closed=True,facecolor='none',linewidth=3))

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
                    tri1.append([q,r])
                if (hex_center[1]>=slope_left[1]*(hex_center[0]-x)+y and
                        hex_center[1]>=slope_bottom[1]*(hex_center[0]-pts_list[4][0])+pts_list[4][1] and
                        hex_center[1]<=slope_right[1]*(hex_center[0]-x)+y):
                    hexes.append([q,r])
                    tri_hexes.append([q,r])
#                    tri_hexes2.append([q,r])
                    polygon = mpatches.RegularPolygon(hex_center, 6, size, color='green', ec='black')
                    patches.append(polygon)
                    counter += 1
                    tri2.append([q,r])
                if (hex_center[1]>=slope_left[2]*(hex_center[0]-x)+y and
                        hex_center[1]<=slope_bottom[2]*(hex_center[0]-pts_list[5][0])+pts_list[5][1] and
                        hex_center[1]<=slope_right[2]*(hex_center[0]-x)+y):
                    hexes.append([q,r])
                    tri_hexes.append([q,r])
#                    tri_hexes2.append([q,r])
                    polygon = mpatches.RegularPolygon(hex_center, 6, size, color='red', ec='black')
                    patches.append(polygon)
                    counter += 1
#                    tri3.append([q,r])
                if (hex_center[1]>=slope_left[3]*(hex_center[0]-x)+y and
                        hex_center[1]<=slope_bottom[3]*(hex_center[0]-pts_list[0][0])+pts_list[0][1] and
                        hex_center[1]>=slope_right[3]*(hex_center[0]-x)+y):
                    hexes.append([q,r])
                    tri_hexes.append([q,r])
#                    tri_hexes2.append([q,r])
                    polygon = mpatches.RegularPolygon(hex_center, 6, size, color='cyan', ec='black')
                    patches.append(polygon)
                    counter += 1
                    tri4.append([q,r])
                if (hex_center[1]<=slope_left[4]*(hex_center[0]-x)+y and
                        hex_center[1]<=slope_bottom[4]*(hex_center[0]-pts_list[1][0])+pts_list[1][1] and
                        hex_center[1]>=slope_right[4]*(hex_center[0]-x)+y):
                    hexes.append([q,r])
                    tri_hexes.append([q,r])
#                    tri_hexes2.append([q,r])
                    polygon = mpatches.RegularPolygon(hex_center, 6, size, color='magenta', ec='black')
                    patches.append(polygon)
                    counter += 1
                    tri5.append([q,r])
                if (hex_center[1]<=slope_left[5]*(hex_center[0]-x)+y and
                        hex_center[1]>=slope_bottom[5]*(hex_center[0]-pts_list[2][0])+pts_list[2][1] and
                        hex_center[1]>=slope_right[5]*(hex_center[0]-x)+y):
                    hexes.append([q,r])
                    tri_hexes.append([q,r])
#                    tri_hexes2.append([q,r])
                    polygon = mpatches.RegularPolygon(hex_center, 6, size, color='yellow', ec='black')
                    patches.append(polygon)
                    counter += 1
#                    tri6.append([q,r])


                # Tile remaining hexagonal grid (blank)
#                else:
#                        hexes.append([q,r])
#                        polygon2 = mpatches.RegularPolygon(hex_center, 6, size, color='none', ec='black')
#                        patches.append(polygon2)
#                        counter2 += 1

def my_compare_c4(x,y):
    if (x[1] < y[1]):
        return -1
    elif (x[1] > y[1]):
        return 1
    elif (x[1] == y[1]):
        return y[0] - x[0]

tri1 = sorted(tri1, key=itemgetter(1), reverse=True)
tri2 = sorted(tri2, key=itemgetter(0,1))
tri4 = sorted(tri4, cmp=my_compare_c4)
tri5 = sorted(tri5, key=itemgetter(0,1), reverse=True)

tri2_diff = tri2[len(tri2)-1][0]-tri2[0][0]+1
print tri2_diff
tri3_start = [tri2[0][0],tri2[0][1]+1]
print tri3_start

for i in range(0,tri2_diff+1):
    k = i
    l = 0
    for j in range(0,i+1):
        q = tri3_start[0] + k
        k  = k - 1
        r = tri3_start[1] + l
        l = l + 1
        tri3.append([q,r])

tri5_diff = tri5[0][0]+1-tri5[len(tri5)-1][0]
print tri5_diff
tri5_start = [tri5[0][0]+1,tri5[0][1]-1]
print tri5_start

for i in range(0,tri5_diff+1):
    k = i
    l = 0
    for j in range(0,i+1):
        q = tri5_start[0] - k
        k  = k - 1
        r = tri5_start[1] - l
        l = l + 1
        tri6.append([q,r])


# Random Number Generator


def focal_coord(x_prime,y_prime):

    q,r = crt2ax(x_prime,y_prime,size)
    hex_center = drawConvert(q,r,size)

    if (hex_center[1]<=slope_left[0]*(hex_center[0]-x)+y and
        hex_center[1]>=slope_bottom[0]*(hex_center[0]-pts_list[3][0])+pts_list[3][1] and
        hex_center[1]<=slope_right[0]*(hex_center[0]-x)+y):
        print [[x_prime,y_prime],1,tri1.index([q,r])+1]

    if (hex_center[1]>=slope_left[1]*(hex_center[0]-x)+y and
        hex_center[1]>=slope_bottom[1]*(hex_center[0]-pts_list[4][0])+pts_list[4][1] and
        hex_center[1]<=slope_right[1]*(hex_center[0]-x)+y):
        print [[x_prime,y_prime],2,tri2.index([q,r])+1]

    if (hex_center[1]>=slope_left[2]*(hex_center[0]-x)+y and
        hex_center[1]<=slope_bottom[2]*(hex_center[0]-pts_list[5][0])+pts_list[5][1] and
        hex_center[1]<=slope_right[2]*(hex_center[0]-x)+y):
        print [[x_prime,y_prime],3,tri3.index([q,r])+1]

    if (hex_center[1]>=slope_left[3]*(hex_center[0]-x)+y and
        hex_center[1]<=slope_bottom[3]*(hex_center[0]-pts_list[0][0])+pts_list[0][1] and
        hex_center[1]>=slope_right[3]*(hex_center[0]-x)+y):
        print [[x_prime,y_prime],4,tri4.index([q,r])+1]

    if (hex_center[1]<=slope_left[4]*(hex_center[0]-x)+y and
        hex_center[1]<=slope_bottom[4]*(hex_center[0]-pts_list[1][0])+pts_list[1][1] and
        hex_center[1]>=slope_right[4]*(hex_center[0]-x)+y):
        print [[x_prime,y_prime],5,tri5.index([q,r])+1]

    if (hex_center[1]<=slope_left[5]*(hex_center[0]-x)+y and
        hex_center[1]>=slope_bottom[5]*(hex_center[0]-pts_list[2][0])+pts_list[2][1] and
        hex_center[1]>=slope_right[5]*(hex_center[0]-x)+y):
        print [[x_prime,y_prime],6,tri6.index([q,r])+1]

#for i in range(0,pt_num):
#    x_prime = (random.uniform(2, bound-2))
#    y_prime = (random.uniform(2, bound-2))
#    plt.plot(x_prime, y_prime, 'bo')
#    focal_coord(x_prime,y_prime)

i_loop = 0
final_countdown = 0
while (i_loop < pt_num):
    try:
        x_prime = (random.uniform(2, bound-2))
        y_prime = (random.uniform(2, bound-2))
        #plt.plot(x_prime, y_prime, 'bo')
        focal_coord(x_prime,y_prime)
        i_loop = i_loop + 1
    except (ValueError):
        i_loop = i_loop + 1
        print 'WHOA',[[x_prime, y_prime],crt2ax(x_prime,y_prime,size)]
        final_countdown = final_countdown + 1
        continue


print 'hex in wedge ',counter
print 'hex not in wedge ',counter2
print 'not captured points', final_countdown
print Counter(hex_list)

#print tri1
#print("\n")
#print tri2
#print("\n")
#print tri3
#print("\n")
#print tri4
#print("\n")
#print tri5
#print("\n")
#print tri6


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
