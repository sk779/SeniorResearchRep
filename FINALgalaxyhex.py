import random
import numpy as np
from hex_coordinates import *
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
from collections import Counter
import math
import pandas

###############

size=50 #in Megaparsecs
npts=500 # number of points
# File
readdata = np.genfromtxt('/Users/shibikannan/Desktop/SeniorResearch/galaxyhex.csv', delimiter = ',')

def AxialConvert(x,y,s):
    q,r = approxAx(x, y, s)
    x,y,z = ax2cb(q,r)
    x,y,z = hexRound(x,y,z)
    return cb2ax(x,y,z)
    
file_x = [] 
file_y = [] 

for i in range(1,npts):
    file_x.append(readdata[i][4])
    file_y.append(readdata[i][5])
        
dict = {}

for i in range(0,npts-1):
    x = file_x[i]
    y = file_y[i]
    q,r = AxialConvert(x,y,size)
    rest_q,rest_r = (q+1000,r+1000)
    if (q,r) in dict.keys():
        if len(dict[(q,r)]) < 5:
            dict[(q,r)].append((x,y))
        #else:
        #    if (rest_q,rest_r) in dict.keys():
        #        dict[(rest_q,rest_r)].append((x,y))
        #    else:
        #        dict[(d,e)] = [(x,y)]
    else:
        dict[(q,r)] = [(x,y)]
            
q_list = [i[0] for i in dict.keys()]
r_list = [i[1] for i in dict.keys()]
gal_hex = []
x_list = []
y_list = []
gal_sum = 0
  
for k in dict.values():
    for l in k:
        x_list.append(l[0])
        y_list.append(l[1])

for p in dict.keys():
    #if p[0] < 50:
    gal_hex.append([p,len(dict[p])])
    gal_sum = gal_sum + len(dict[p])
    #else:
    #    nogal_hex.append([p,len(dict[p])])
    ##gal_hex2.append(len(dict[p]))

print "Counted X"
print x_list
print "Counted Y"
print y_list
print "Count Per Hex"
print gal_hex
print "Total Hex Count is",gal_sum
