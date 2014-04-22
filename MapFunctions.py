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

# Function that finds big hex position for point
def convert(x_prime,y_prime,rad,x_start,y_start,hex_num):
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

def convert2(x_prime,y_prime,rad,x_start,y_start,hex_num):
	x_start = x_start - rad
	y_start = y_start - (math.sqrt(3)/2)*rad
	i_pos = -1
	j_pos = -1
	for i in range(0,hex_num):
		x_left = x_start + 2*rad*i
		x_right = x_start + 2*rad*(i+1)
		if ((x_prime > x_left) and (x_prime < x_right)):
		    i_pos = i
		    break
	for j in range(0,hex_num):
		y_left = y_start + (math.sqrt(3)*rad*j)
		y_right = y_start + (math.sqrt(3)*rad*(j+1))
		if ((y_prime > y_left) and (y_prime < y_right)):
		    j_pos = j
		    break
	if ((i_pos >= 0) and (j_pos >= 0)):
		return x_prime, y_prime, (j_pos, i_pos)

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

def square_convert2(x_prime, y_prime,x_start,y_start,sq_size,lim):
    i_pos = 0
    j_pos = 0
    for i in range(0,lim):
        x_left = x_start + sq_size*i
        x_right = x_start + sq_size*(i+1)
        if ((x_prime > x_left) and (x_prime < x_right)):
            i_pos = i
            break
    for j in range(0,lim):
        y_left = y_start + sq_size*j
        y_right = y_start + sq_size*(j+1)
        if ((y_prime > y_left) and (y_prime < y_right)):
            j_pos = j
            break
    return (i_pos,j_pos)



def dynamic_tri_list_start(x, y, radius, bound, size):
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
	n= 2*bound


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

	q_list = []
	r_list = []

	for r in range(-n,n):
		for q in range(-n,n):
			hex_center = drawConvert(q,r,size)
			if (abs(hex_center[0])<bound+size and abs(hex_center[1])<bound+size and hex_center[0]>=0 and hex_center[1]>=0):
				for i in range(0,6):
					if (ops[slopeleft_ineq[i]](hex_center[1],slope_left[i]*(hex_center[0]-x)+y) and
					ops[slopebottom_ineq[i]](hex_center[1],slope_bottom[i]*(hex_center[0]-pts_list[i][0])+pts_list[i][1]) and
					ops[sloperight_ineq[i]](hex_center[1],slope_right[i]*(hex_center[0]-x)+y)):
						# polygon = mpatches.RegularPolygon(hex_center, 6, size, color=color_list[i], ec='black')
						# patches.append(polygon)
						q_list.append(q)
						r_list.append(r)
						if (i != 2 and i != 5):
							tri_list[i].append([q,r])
						counter = counter+1

	return min(q_list), min(r_list), max(q_list), max(r_list)

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
	n= 2*bound


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

	q_list = []
	r_list = []

	for r in range(-n,n):
		for q in range(-n,n):
			hex_center = drawConvert(q,r,size)
			# if (abs(hex_center[0])<bound+size and abs(hex_center[1])<bound+size and hex_center[0]>=0 and hex_center[1]>=0):
			for i in range(0,6):
				if (ops[slopeleft_ineq[i]](hex_center[1],slope_left[i]*(hex_center[0]-x)+y) and
				ops[slopebottom_ineq[i]](hex_center[1],slope_bottom[i]*(hex_center[0]-pts_list[i][0])+pts_list[i][1]) and
				ops[sloperight_ineq[i]](hex_center[1],slope_right[i]*(hex_center[0]-x)+y)):
					# polygon = mpatches.RegularPolygon(hex_center, 6, size, color=color_list[i], ec='black')
					# patches.append(polygon)
					q_list.append(q)
					r_list.append(r)
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
	# print tri_list
	print len(tri_list[0]),len(tri_list[1]),len(tri_list[2]),len(tri_list[3]),len(tri_list[4]),len(tri_list[5])
	print min(q_list), min(r_list), max(q_list), max(r_list)
	return tri_list

def dynamic_tri_list2(x, y, radius, q_min, q_max, r_min,r_max, size):
	# print x,y,radius,q_min,q_max,r_min,r_max,size
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

	for r in range(int(r_min),int(r_max)):
		for q in range(int(q_min),int(q_max)):
			hex_center = drawConvert(q,r,size)
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
	# print tri_list
	print len(tri_list[0]),len(tri_list[1]),len(tri_list[2]),len(tri_list[3]),len(tri_list[4]),len(tri_list[5])
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