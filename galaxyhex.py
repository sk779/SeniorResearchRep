import random
import numpy as np
from hex_coordinates import *
import matplotlib.pyplot as plt; plt.rcdefaults()
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
from collections import Counter
import math

def buildHexes(size):
	fig, ax = plt.subplots()
	patches = []
	hexes = []
	bound = 1000
	n = 2*bound/size
	for r in range(-n,n):
		for q in range(-n,n):
				hex_center = drawConvert(q,r,size)
				if (abs(hex_center[0])<bound+size and abs(hex_center[1])<bound+size and hex_center[0]>=0 and hex_center[1]>=0):
					hexes.append([q,r])
					polygon = mpatches.RegularPolygon(hex_center, 6, size, fill=False)
					patches.append(polygon)
	return hexes, patches, ax

def crt2ax(x,y,s):
	q,r = approxAx(x, y, s)
	x,y,z = ax2cb(q,r)
	x,y,z = hexRound(x,y,z)
	return cb2ax(x,y,z)

def plotGals(npts):
	color=['go']*npts
	hex_counts = [0]*(len(hexes)+1)
	for i in range(1,npts-1):
		x = gals[i][1]
		y = gals[i][2]
		q,r = crt2ax(x,y,size)
		#hexes[i] = [q,r]
		try:
			index = hexes.index([q,r])
		except:
			index = len(hexes)
		hex_counts[index] += 1
		plt.plot(x,y,color[i])

	collection = PatchCollection(patches, cmap=plt.cm.hsv, alpha=0.3, match_original=True)
	ax.add_collection(collection)
	plt.axis([0,1000,0,1000])
	plt.plot(0,0,'b*')
	plt.show()
	return hex_counts

def pruneGals(ngal):
	for i in range(len(hexes)):
		if hex_counts[i] > ngal:
			hex_counts[i] = ngal
	return hex_counts


# Input parameters
size = 20 #in Megaparsecs
npts = 3000 # number of points
ngal = 5
gals = np.load('gal_locs.npy')

hexes,patches,ax = buildHexes(size)
hex_counts = plotGals(npts)
pruneGals(ngal)

# printlist = []
# for i in range(len(hexes)):
# 	if hex_counts[i] > 0:
# 		printlist.append([hexes[i],hex_counts[i]])

# histdata = Counter(hex_counts)
# print histdata.most_common()
# print printlist, sum(hex_counts)
# plt.hist(hex_counts,bins=[1,2,3,4,5,6])
# plt.show()
