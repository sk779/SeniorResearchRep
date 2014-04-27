import random
import numpy as np
from hex_coordinates import *
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

# Main

radius = 1.49270533036  # focal plane radius (70 for 5000)
x = radius+.1  # starting x
y = radius+.1 # starting y
grid_lim = 100 # number of x/y bins in heatmap
size = 0.02015 # fiber size (1 for 5000)
pt_num = 1 # number of points (galaxies) to test
hex_num = 10 # number of focal plane iterations across heatmap
x_hex_num = 2
y_hex_num = 2
graph_bound = 25.0 # range of graph
bound = 200 # fix at 200

fig, ax = plt.subplots()
i_loop = 0
error_count = 0
random.seed(5)
patches = []
dict = {}
tri_dict = {}
square_dict = {}
total_square_dict = {}
all_pt_list = []

# Establish fiber order/location for each focal plane position

q_r_stuff = dynamic_tri_list_start(x, y, radius, bound, size)
q_start = q_r_stuff[0]
r_start = q_r_stuff[1]
q_diff = q_r_stuff[2] - q_r_stuff[0]
r_diff = q_r_stuff[3] - q_r_stuff[1]


for j in range(0,y_hex_num):
    for i in range(0, x_hex_num):
        print j,i
        new_x = x + ((2*radius*i))/2
        new_y = y + ((math.sqrt(3)*radius*j))
        q_min = (q_start + (q_diff*i)/2) - 50 - (.5*q_diff*j)
        q_max = (q_start + (q_diff*(i+1))/2) + 50 - (.5*q_diff*j)
        r_min = r_start + (r_diff*j) - 50
        r_max = r_start + (r_diff*(j+1)) + 50
        print q_min, q_max, r_min, r_max
        polygon = mpatches.RegularPolygon([new_x,new_y], 6, radius, (math.pi)/2, linewidth=1,color='none', ec='black')
        patches.append(polygon)
        tri_dict[(j,i)] = []
        tri_dict[(j,i)].append(dynamic_tri_list2(new_x, new_y, radius, q_min, q_max, r_min,r_max, size))

# Run points to determine where they fall in focal plane positions
while (i_loop < pt_num):
    try:
        # x_prime_old, y_prime_old = random.uniform(0,graph_bound), random.uniform(0,graph_bound)
        x_prime_old, y_prime_old = 3.3123,3.5243
        x_prime, y_prime, plane_number = convert2(x_prime_old,y_prime_old,radius,x,y,x_hex_num,y_hex_num)
        new_x = x + (2*radius*plane_number[1])/2
        new_y = y + (math.sqrt(3)*radius*plane_number[0])
        coord = new_focal_coord(x_prime,y_prime,radius,new_x,new_y,size,tri_dict[(plane_number[0],plane_number[1])])
        coord2 = coord[0], coord[1],plane_number[0],plane_number[1]
        if coord2 in dict.keys():
            if len(dict[coord2]) < 2:
                dict[coord2].append((x_prime,y_prime))
        else:
            dict[coord2] = [(x_prime,y_prime)]
        if (i_loop % 1000 == 0):
            print i_loop    
        i_loop = i_loop + 1
        all_pt_list.append([x_prime_old,y_prime_old])
    except (ValueError,TypeError):
        all_pt_list.append([x_prime_old,y_prime_old])
        i_loop = i_loop + 1
        error_count = error_count + 1
        continue

all_pt_x = tuple(x[0] for x in all_pt_list)
all_pt_y = tuple(x[1] for x in all_pt_list)
val_list = list(dict.values())
val_list = [x for y in val_list for x in y]
x_list = tuple(x[0] for x in val_list)
y_list = tuple(x[1] for x in val_list)

# Heat map code

for i in range(0,len(x_list)):
    if (i % 1000 == 0):
        print i   
    square_number = square_convert2(x_list[i],y_list[i],0,0,float(graph_bound/grid_lim),grid_lim)
    if square_number in square_dict.keys():
        square_dict[square_number].append([(x_list[i],y_list[i])])
    else:
        square_dict[square_number] = [(x_list[i],y_list[i])]

for i in range(0,len(all_pt_x)):
    if (i % 1000 == 0):
        print i   
    square_number = square_convert2(all_pt_x[i],all_pt_y[i],0,0,float(graph_bound/grid_lim),grid_lim)
    if square_number in total_square_dict.keys():
        total_square_dict[square_number].append([(all_pt_list[i][0],all_pt_list[i][1])])
    else:
        total_square_dict[square_number] = [(all_pt_list[i][0],all_pt_list[i][1])]

# Takes care of heat map bins with no pts (small error correction)
dict_sum = 0
dict_sum2 = 0;
i_dict = 0
while (i_dict < grid_lim):
    j_dict = 0
    while (j_dict < grid_lim):
        try:
            dict_sum = dict_sum + len(square_dict[i_dict, j_dict]);
            dict_sum2 = dict_sum2 + len(total_square_dict[i_dict, j_dict]);
            j_dict = j_dict + 1
        except (KeyError):
            square_dict[(i_dict,j_dict)] = []
            total_square_dict[(i_dict,j_dict)] = []
            j_dict = j_dict + 1
    i_dict = i_dict+1

# Heatmap Plotting
x_list2 = []
y_list2 = []
val_list2 = []
capture_list = []
all_list = []

j_stuff = 0
while (j_stuff < grid_lim):
    if (j_stuff % 50):
        print j_stuff
    i_stuff = 0
    while (i_stuff < grid_lim): 
        try:
            x_list2.append((graph_bound/grid_lim)*i_stuff+.5*(graph_bound/grid_lim))
            y_list2.append((graph_bound/grid_lim)*j_stuff+.5*(graph_bound/grid_lim))
            val_list2.append(len(square_dict[(i_stuff,j_stuff)]))
            q = float(len(square_dict[(i_stuff,j_stuff)]))
            r = float(len(total_square_dict[(i_stuff,j_stuff)]))
            all_list.append(r)
            capture_list.append((q/r)*100)
            print j_stuff, " ", i_stuff, " ", (q/r)*100, "%"
            i_stuff = i_stuff +1
        except (ZeroDivisionError):
            capture_list.append(0)
            # print j_stuff, " ", i_stuff, " ", 0
            i_stuff = i_stuff +1
    j_stuff = j_stuff + 1

# Table of values in each heatmap position
print "Total points", dict_sum2
print "Points captured: ", dict_sum
print "Points out of range: ", error_count

# for j_dict_2 in range(0,grid_lim):
#     for i_dict_2 in range(0,grid_lim):
#         print i_dict_2, " ", j_dict_2, " ", (float(len(square_dict[(i_stuff,j_stuff)]))/float(len(total_square_dict[(i_stuff,j_stuff)])))*100



plt.axes().set_aspect('equal')
plt.scatter(x_list2, y_list2, c=capture_list, s=550, marker=(4, 0, 45))
plt.xlim(0, graph_bound)
plt.ylim(0, graph_bound)
cb = plt.colorbar()
cb.set_label('capture value (%)')
collection = PatchCollection(patches, cmap=plt.cm.hsv, alpha=0.3, match_original=True)
ax.add_collection(collection)
plt.show()

plt.hist(capture_list, range=[0, 100], bins=20)
plt.show()