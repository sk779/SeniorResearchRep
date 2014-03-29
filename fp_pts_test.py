import numpy as np
from hex_coordinates import *
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt; plt.rcdefaults()

fig, ax = plt.subplots()
patches = []

bound = 1000
npts = 10000 # number of points (3845257)

fp_radius = 100
nfp = 100
fp_x = 1000*np.random.rand(nfp)
fp_y = 1000*np.random.rand(nfp)

def inFocalPlane(gx,gy,fpx,fpy,fpr):
	obs = 0
	for i in range(nfp):
		x = gx-fpx[i]
		y = gy-fpy[i]
		q,r = crt2ax(x,y,fpr)
		obs = obs + ((q,r)==(0,0))
	return obs

gal_weights = np.ones(npts)
for i in range(npts):
	if i%1000==0: print i
	x = np.random.uniform(0,bound)
	y = np.random.uniform(0,bound)
	gal_weights[i] = inFocalPlane(x,y,fp_x,fp_y,fp_radius)
	col = gal_weights[i]/10.
	_ = plt.plot(x,y,color=str(col),marker='o');

print max(gal_weights)
plt.show()


