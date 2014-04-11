import random
import numpy as np
from hex_coordinates import *
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
from collections import Counter
import math
import pandas
from matplotlib.patches import Polygon, Circle
from operator import itemgetter, attrgetter
import operator
from matplotlib.path import Path
from matplotlib import cm as CM

# Global Variables/Initializations

# Seed Initialization
random.seed(1)

fig, ax = plt.subplots()
patches = []
pts_list=[]
slope_right=[]
slope_bottom=[]
slope_left=[]
slopeleft_ineq=["<=",">=",">=",">=","<=","<="]
slopebottom_ineq=[">=",">=","<=","<=","<=",">="]
sloperight_ineq=["<=","<=","<=",">=",">=",">="]
hex_list = []
tri_list = [[] for i in range(6)]
dict = {}

# Hex Geometry (Cartesian -> Axial)
def crt2ax(x,y,size):
    q,r = approxAx(x, y, size)
    x,y,z = ax2cb(q,r)
    x,y,z = hexRound(x,y,z)
    return cb2ax(x,y,z)

# Define Operators

ops = {"<=": operator.le, ">=": operator.ge}


bound = 100
hex_num = 6

n= 2*bound
size=1

radius = 10
x = 25
y = 25


# Determine Hex Vertices

for k in range(0,6):
    pts_list.append([(x + radius*math.cos((2*math.pi*(k+1))/6)),(y + radius*math.sin((2*math.pi*(k+1))/6))])

pts_list[3],pts_list[0] = pts_list[0],pts_list[3]
pts_list[4],pts_list[1] = pts_list[1],pts_list[4]
pts_list[5],pts_list[2] = pts_list[2],pts_list[5]

# Slopes of triangles

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

# Hexagonal Grid Drawing

for r in range(-n,n):
	for q in range(-n,n):
            hex_center = drawConvert(q,r,size)
            if (abs(hex_center[0])<bound+size and abs(hex_center[1])<bound+size and hex_center[0]>=0 and hex_center[1]>=0):
                for i in range(0,6):
                    if (ops[slopeleft_ineq[i]](hex_center[1],slope_left[i]*(hex_center[0]-x)+y) and
                        ops[slopebottom_ineq[i]](hex_center[1],slope_bottom[i]*(hex_center[0]-pts_list[i][0])+pts_list[i][1]) and
                        ops[sloperight_ineq[i]](hex_center[1],slope_right[i]*(hex_center[0]-x)+y)):
                            if (i != 2 and i != 5):
                                tri_list[i].append([q,r])

# Create consistent numbering scheme for hexagons within each wedge of focal plane

# Tri 1, 2, 5
tri_list[0] = sorted(tri_list[0], key=itemgetter(1), reverse=True)
tri_list[1] = sorted(tri_list[1], key=itemgetter(0,1))
tri_list[4] = sorted(tri_list[4], key=itemgetter(0,1), reverse=True)

# Tri 3
tri_list1_diff = tri_list[1][len(tri_list[1])-1][0]-tri_list[1][0][0]+1
tri_list2_start = [tri_list[1][0][0],tri_list[1][0][1]+1]

for i in range(0,tri_list1_diff+1):
    k = i
    l = 0
    for j in range(0,i+1):
        q = tri_list2_start[0] + k
        k  = k - 1
        r = tri_list2_start[1] + l
        l = l + 1
        tri_list[2].append([q,r])

# Tri 4
def my_compare_c4(x,y):
    if (x[1] < y[1]):
        return -1
    elif (x[1] > y[1]):
        return 1
    elif (x[1] == y[1]):
        return y[0] - x[0]
tri_list[3] = sorted(tri_list[3], cmp=my_compare_c4)

#Tri 6
tri_list4_diff = tri_list[4][0][0]+1-tri_list[4][len(tri_list[4])-1][0]
tri_list4_start = [tri_list[4][0][0]+1,tri_list[4][0][1]-1]

for i in range(0,tri_list4_diff+1):
    k = i
    l = 0
    for j in range(0,i+1):
        q = tri_list4_start[0] - k
        k  = k - 1
        r = tri_list4_start[1] - l
        l = l + 1
        tri_list[5].append([q,r])

# Function that maps cartesian to focal plane coordinates
def focal_coord(x_prime,y_prime):
    q,r = crt2ax(x_prime,y_prime,size)
    hex_center = drawConvert(q,r,size)
    for i in range(0,6):
        if (ops[slopeleft_ineq[i]](hex_center[1],slope_left[i]*(hex_center[0]-x)+y) and
            ops[slopebottom_ineq[i]](hex_center[1],slope_bottom[i]*(hex_center[0]-pts_list[i][0])+pts_list[i][1]) and
            ops[sloperight_ineq[i]](hex_center[1],slope_right[i]*(hex_center[0]-x)+y)):
            print [[x_prime,y_prime],[q,r],i+1,tri_list[i].index([q,r])+1]

# Function that tells which focal plane position (given by j,i) any point corresponds to
for j in range(0,hex_num):
    for i in range (0,hex_num):
        x_center = x + 2*radius*i
        y_center = y + math.sqrt(3)*radius*j
        polygon = mpatches.RegularPolygon([x_center,y_center], 6, radius, (math.pi)/2, color='none', ec='black')
        patches.append(polygon)

# Function that determines what big hex each point is in
def convert(x_prime,y_prime):
    g = -1
    for j in range(0,hex_num):
        for i in range (0,hex_num):
            vertex_set = []
            x_center = x+(radius*2*i)
            y_center = y+(radius*math.sqrt(3)*j)
            for k in range(0,6):
                vertex_set.append([x_center+radius*math.cos((2*math.pi*k)/6),y_center+radius*math.sin((2*math.pi*k)/6)])
            vertex_path = Path(vertex_set)
            result = vertex_path.contains_point([x_prime,y_prime],radius=0.1)
            g = g+1
            if (result==1):
                # print x_prime, y_prime, (j, i)
                return x_prime, y_prime, (j, i)

plt.axes().set_aspect('equal', 'datalim')
collection = PatchCollection(patches, cmap=plt.cm.hsv, alpha=0.3, match_original=True)
ax.add_collection(collection)
plt.axis([-50,100,-50,100])
plt.show()

