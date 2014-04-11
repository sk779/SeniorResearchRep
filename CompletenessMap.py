import random
import numpy as np
from hex_coordinates import *
# from FinalHeatmapCode_VaryHex import *
from MapFunctions import *
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

# Function that finds big hex position for point
def convert(x_prime,y_prime,rad,x_start,y_start):
    for j in range(0,hex_num):
        for i in range (0,hex_num):
            vertex_set = []
            x_square = x_start+(rad*2*i)
            y_square = y_start+(rad*math.sqrt(3)*j)
            for k in range(0,6):
                vertex_set.append([x_square+rad*math.cos((2*math.pi*k)/6),y_square+rad*math.sin((2*math.pi*k)/6)])
            vertex_path = Path(vertex_set)
            result = vertex_path.contains_point([x_prime,y_prime],radius=0.1)
            if (result==1):
                # print (j,i)
                return x_prime, y_prime, (j, i)

# Function that finds heat map bin position for point
def square_convert(x_prime, y_prime,x_start,y_start,sq_size,lim):
    for j in range(0,lim):
        for i in range(0,lim):
            vertex_set = []
            x_square = x_start + sq_size*i
            y_square = y_start + sq_size*j
            vertex_set.append([x_square,y_square])
            vertex_set.append([x_square,y_square+sq_size])
            vertex_set.append([x_square+sq_size,y_square+sq_size])
            vertex_set.append([x_square+sq_size,y_square])
            vertex_path = Path(vertex_set)
            result = vertex_path.contains_point([x_prime,y_prime],radius=0.1)
            if (result==1):
                return (i, j)

# Main

# x = 70.1 # starting x
# y = 70.1 # starting y
# grid_lim = 5 # number of x/y bins in heatmap
# radius = 70 # focal plane radius (70 for 5000)
# size = 1 # fiber size (1 for 5000)
# pt_num = 10000 # number of points (galaxies) to test
# hex_num = 2 # number of focal plane iterations across heatmap
# bound = 300 # bound of x/y canvas

x = 10.1 # starting x
y = 10.1 # starting y
grid_lim = 25 # number of x/y bins in heatmap
radius = 10 # focal plane radius (70 for 5000)
size = 1 # fiber size (1 for 5000)
pt_num = 1000 # number of points (galaxies) to test
hex_num = 2 # number of focal plane iterations across heatmap
bound = 50 # bound of x/y canvas

i_loop = 0
error_count = 0
random.seed(1)
big_tri_list = [[] for i in range(hex_num)]
#big_tri_list = []
patches = []

dict = {}
tri_dict = {}

# Establish fiber order/location for each focal plane position
for j in range(0,hex_num):
    for i in range(0, hex_num):
        print j,i
    	new_x = x + 2*radius*i
    	new_y = y + math.sqrt(3)*radius*j
        tri_dict[(j,i)] = []
        tri_dict[(j,i)].append(dynamic_tri_list(new_x, new_y, radius, bound, size))
        # if (j,i) in tri_dict.keys():
        #     tri_dict[(j,i)].append(dynamic_tri_list(new_x, new_y, radius, bound, size))
        # else:
        #     tri_dict[(j,i)] = []
        #big_tri_list[j][i].append(dynamic_tri_list(new_x, new_y, radius, bound, size))
    	#big_tri_list.append(dynamic_tri_list(new_x, new_y, radius, bound, size))

# print tri_dict[(0,0)]
# print tri_dict.keys()

# focal_coord(39.0231,20.8389, radius, 45,y,size,big_tri_list[1])

# Run points to determine where they fall in focal plane positions
while (i_loop < pt_num):
    try:
        x_prime_old, y_prime_old = random.uniform(0,bound), random.uniform(0,bound)
        x_prime, y_prime, plane_number = convert(x_prime_old,y_prime_old,radius,x,y)
        new_x = x + 2*radius*plane_number[1]
        new_y = y + math.sqrt(3)*radius*plane_number[0]
        # plt.scatter(x_prime_old, y_prime_old, color = 'blue')
        # print plane_number[0], plane_number[1]
        coord = new_focal_coord(x_prime,y_prime,radius,new_x,new_y,size,tri_dict[(plane_number[0],plane_number[1])])
        coord2 = coord[0], coord[1],plane_number[0], plane_number[1]
        # now find which of the fibers has been hit
        # print coord2
        if coord2 in dict.keys():
            if len(dict[coord2]) < 2:
                dict[coord2].append((x_prime,y_prime))
        else:
            dict[coord2] = [(x_prime,y_prime)]
        if (i_loop % 10 == 0):
            print i_loop    
        i_loop = i_loop + 1
    except (ValueError,TypeError):
        # plt.scatter(x_prime_old, y_prime_old, color = 'green')
        i_loop = i_loop + 1
        error_count = error_count + 1
        continue

# print dict
# print dict.keys()

square_dict = {}

val_list = list(dict.values())
# print val_list
val_list = [x for y in val_list for x in y]
# print val_list
# print dict
x_list = tuple(x[0] for x in val_list)
y_list = tuple(x[1] for x in val_list)

# print x_list
# print y_list

# Heat map code
for i in range(0,len(x_list)):
    if (i % 10 == 0):
        print i   
    square_number = square_convert(x_list[i],y_list[i],0,0,(bound/grid_lim),grid_lim)
    if square_number in square_dict.keys():
        square_dict[square_number].append([(x_list[i],y_list[i])])
    else:
        square_dict[square_number] = [(x_list[i],y_list[i])]

# print square_dict

# Takes care of heat map bins with no pts (small error correction)
dict_sum = 0
i_dict = 0
while (i_dict < grid_lim):
    j_dict = 0
    while (j_dict < grid_lim):
        try:
            dict_sum = dict_sum + len(square_dict[i_dict, j_dict]);
            j_dict = j_dict + 1
        except (KeyError):
            square_dict[(i_dict,j_dict)] = []
            j_dict = j_dict + 1
    i_dict = i_dict+1

# Heatmap Plotting
x_list2 = []
y_list2 = []
val_list2 = []
for j in range(0,grid_lim):
    for i in range(0, grid_lim):
        x_list2.append((bound/grid_lim)*i+.5*(bound/grid_lim))
        y_list2.append((bound/grid_lim)*j+.5*(bound/grid_lim))
        val_list2.append(len(square_dict[(i,j)]))

# Table of values in each heatmap position
print "Points in range: ", dict_sum
print "Points out of range: ", error_count
prob_sum = 0
for j_dict in range(0,grid_lim):
    for i_dict in range(0,grid_lim):
        prob_sum = prob_sum + len(square_dict[(i_dict,j_dict)])/float(pt_num)
        print i_dict, " ", j_dict, " ",len(square_dict[i_dict, j_dict])," ",len(square_dict[(i_dict,j_dict)])/float(pt_num)

plt.scatter(x_list2, y_list2, c=val_list2, s=50, marker=(4, 0, 45))
plt.xlim(0, bound)
plt.ylim(0, bound)
cb = plt.colorbar()
cb.set_label('capture value')
plt.show()
