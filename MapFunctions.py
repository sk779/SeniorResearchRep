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

ops = {"<=": operator.le, ">=": operator.ge}
slopeleft_ineq=["<=",">=",">=",">=","<=","<="]
slopebottom_ineq=[">=",">=","<=","<=","<=",">="]
sloperight_ineq=["<=","<=","<=",">=",">=",">="]

def dynamic_tri_list(x, y, radius, bound, size):
	slope_right=[]
	slope_bottom=[]
	slope_left=[]
	pts_list=[]
	counter = 0
	# fig, ax = plt.subplots()
	patches = []
	color_list=["blue","green","red","cyan","magenta","yellow"]
	marker_list=["o","s","p","*","D",">"]
	hex_list = []
	tri_list = [[] for i in range(6)]

	# Determine hexagon vertices
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

	for r in range(-(2*bound),(2*bound)):
		for q in range(-(2*bound),(2*bound)):
	            hex_center = drawConvert(q,r,size)
	            if (abs(hex_center[0])<bound+size and abs(hex_center[1])<bound+size and hex_center[0]>=0 and hex_center[1]>=0):
	                for i in range(0,6):
	                    if (ops[slopeleft_ineq[i]](hex_center[1],slope_left[i]*(hex_center[0]-x)+y) and
	                        ops[slopebottom_ineq[i]](hex_center[1],slope_bottom[i]*(hex_center[0]-pts_list[i][0])+pts_list[i][1]) and
	                        ops[sloperight_ineq[i]](hex_center[1],slope_right[i]*(hex_center[0]-x)+y)):
	                           # polygon = mpatches.RegularPolygon(hex_center, 6, size, color=color_list[i], ec='black')
	                           # patches.append(polygon)
	                           if (i != 2 and i != 5):
	                                tri_list[i].append([q,r])
	                            	counter = counter+1

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

	# plt.axes().set_aspect('equal', 'datalim')
	# collection = PatchCollection(patches, cmap=plt.cm.hsv, alpha=0.3, match_original=True)
	# ax.add_collection(collection)
	# plt.axis([-50,100,-50,100])
	# plt.show()

	return tri_list

# Function that maps cartesian to focal plane coordinates
def focal_coord(x_prime,y_prime, radius, x,y,size,tri_list):
	slope_right=[]
	slope_bottom=[]
	slope_left=[]
	pts_list=[]
	q,r = crt2ax(x_prime,y_prime,size)
	hex_center = drawConvert(q,r,size)

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

	print tri_list
	tri_list = [x for y in tri_list for x in y]
	print "WIN", tri_list[0].index([8,14])
	print [[x_prime,y_prime],[q,r]]
	for i in range(0,6):
		if (ops[slopeleft_ineq[i]](hex_center[1],slope_left[i]*(hex_center[0]-x)+y) and ops[slopebottom_ineq[i]](hex_center[1],slope_bottom[i]*(hex_center[0]-pts_list[i][0])+pts_list[i][1]) and ops[sloperight_ineq[i]](hex_center[1],slope_right[i]*(hex_center[0]-x)+y)):
			# plt.plot(x_prime, y_prime, marker=marker_list[i],color='black')
			print "AAHHH"
			print tri_list[i]
			print [[x_prime,y_prime],[q,r],i+1]
			print [[x_prime,y_prime],[q,r],i+1,tri_list[i].index([q,r])+1]
			return [i+1,tri_list[i].index([q,r])+1]


# To determine fiber location of point for any given focal plane
def new_focal_coord(x_prime,y_prime, radius, x,y,size,tri_list):
	q,r = crt2ax(x_prime,y_prime,size)
	tri_list = [x for y in tri_list for x in y]
	i = 0
	while (i < 6):
		if ([q,r] in tri_list[i]):
			# print x_prime, y_prime, i+1, tri_list[i].index([q,r])+1
			return i+1, tri_list[i].index([q,r])+1
		i = i+1
	# for i in range (0,6):
	# 	print [[x_prime,y_prime],[q,r],i+1,tri_list[i].index([q,r])+1 