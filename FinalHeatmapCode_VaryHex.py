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

# Determine big hex for each point

def convert(x_prime,y_prime,rad,x_start,y_start):
    for j in range(0,hex_num):
        for i in range (0,hex_num):
            vertex_set = []
            x_center = x_start+(rad*2*i)
            y_center = y_start+(rad*math.sqrt(3)*j)
            for k in range(0,6):
                vertex_set.append([x_center+rad*math.cos((2*math.pi*k)/6),y_center+rad*math.sin((2*math.pi*k)/6)])
            vertex_path = Path(vertex_set)
            result = vertex_path.contains_point([x_prime,y_prime],radius=0.1)
            if (result==1):
                return x_prime, y_prime, (j, i)

# Sample point distributions
def pt_distrib_steadydec(i_loop,pt_num):
    x_prime = random.uniform(15,bound)
    y_prime = random.uniform(15,(float(i_loop)/float(pt_num))*bound)
    return x_prime, y_prime

def pt_distrib_twoweights(i_loop,pt_num):
    if (i_loop < (pt_num/2)):
        x_prime = random.uniform(15,bound)
        y_prime = random.uniform(15,.5*bound)
    else:
        x_prime = random.uniform(15,bound)
        y_prime = random.uniform(.5*bound,bound)
    return x_prime, y_prime


# Main
radius = 70
x = 80
y = 80
pt_num = 10000
hex_num = 6
bound = hex_num*(500/3)
i_loop = 0
error_count = 0
random.seed(1)
dict = {}
while (i_loop < pt_num):
    try:
        x_prime, y_prime = pt_distrib_steadydec(i_loop,pt_num)
        x_prime, y_prime, plane_number = convert(x_prime,y_prime,radius,x,y)
        if plane_number in dict.keys():
            dict[plane_number].append([(x_prime,y_prime)])
        else:
            dict[plane_number] = [plane_number]
        i_loop = i_loop + 1
    except (ValueError,TypeError):
        i_loop = i_loop + 1
        error_count = error_count + 1
        continue

# Takes care of hexagons with no pts (small error correction)
dict_sum = 0
j_dict = 0
while (j_dict < hex_num):
    i_dict = 0
    while (i_dict < hex_num):
        try:
            dict_sum = dict_sum + len(dict[j_dict, i_dict]);
            i_dict = i_dict + 1
        except (KeyError):
            dict[(j_dict,i_dict)] = []
            i_dict = i_dict + 1
    j_dict = j_dict+1

# Heatmap Plotting
x_list = []
y_list = []
val_list = []
for j in range(0,hex_num):
    for i in range(0, hex_num):
        x_list.append(x + 2*radius*i)
        y_list.append(y + math.sqrt(3)*radius*j)
        val_list.append(len(dict[(j,i)]))

plt.scatter(x_list, y_list, c=val_list, s=50)
plt.xlim(0, bound)
plt.ylim(0, bound)
cb = plt.colorbar()
cb.set_label('capture value')
# plt.show()

# Table of values in each big hex
print "Points in range: ", dict_sum
print "Points out of range: ", error_count
prob_sum = 0
for j_dict in range(0,hex_num):
    for i_dict in range(0,hex_num):
        prob_sum = prob_sum + len(dict[(j_dict,i_dict)])/float(pt_num)
        print j_dict, " ", i_dict, " ",len(dict[j_dict, i_dict])," ",len(dict[(j_dict,i_dict)])/float(pt_num)