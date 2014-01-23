import numpy as np
from hex_coordinates import *
import matplotlib.patches as mpatches

###############

hex_size=8 #in Megaparsecs
npts=30000 # number of points

in_file = '../data/gal_locs.npy'
gals = np.load(in_file)
gals = gals[0:npts]

def crt2ax(x,y,s):
    q,r = approxAx(x, y, s)
    x,y,z = ax2cb(q,r)
    x,y,z = hexRound(x,y,z)
    return cb2ax(x,y,z)

dict = {}
valid = np.ones(npts)
for i in range(npts):
    x = gals[i,1]
    y = gals[i,2]
    q,r = crt2ax(x,y,hex_size)
    if (q,r) in dict.keys():
        if len(dict[(q,r)]) < 5:
            dict[(q,r)].append((x,y))
        else:
            valid[i] = 0
    else:
        dict[(q,r)] = [(x,y)]

pruned_gals = gals[valid==np.ones(npts)]
out_file = '../data/gal_locs_pruned_' + str(npts/1000) + 'k.npy'
np.save(out_file, pruned_gals)



# q_list = [i[0] for i in dict.keys()]
# r_list = [i[1] for i in dict.keys()]
# gal_hex = []
# x_list = []
# y_list = []
# gal_sum = 0
  
# for k in dict.values():
#     for l in k:
#         x_list.append(l[0])
#         y_list.append(l[1])

for p in dict.keys():
    #if p[0] < 50:
    gal_hex.append([p,len(dict[p])])
    gal_sum = gal_sum + len(dict[p])
    #else:
    #    nogal_hex.append([p,len(dict[p])])
    ##gal_hex2.append(len(dict[p]))

# print "Counted X"
# print x_list
# print "Counted Y"
# print y_list
# print "Count Per Hex"
# print gal_hex
# print "Total Hex Count is",gal_sum
