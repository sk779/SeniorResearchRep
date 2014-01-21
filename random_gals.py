import numpy as np
import csv

def getBox(x,y,z,scale):
	box = (int(x)/scale)*(1000/scale)**2+(int(y)/scale)*(1000/scale)+(int(z)/scale)
	return(box)

bound = 1000
npts = 1000000
gals = np.zeros([npts,5])
for i in range(npts):
	x = np.random.uniform(0,bound)
	y = np.random.uniform(0,bound)
	z = np.random.uniform(0,bound)
	box = getBox(x,y,z,100)
	gals[i] = np.array([np.random.uniform(),x,y,z,box])

gals = gals[gals[:,0].argsort()]
out_file = '../data/rand_gals.npy'
np.save(out_file, gals)