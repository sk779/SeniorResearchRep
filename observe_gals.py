import numpy as np
from hex_coordinates import *
import matplotlib.patches as mpatches

###############

hex_size = 1 # in Megaparsecs
nmax = 5 # max gals per hex/fiber
npts = 2000000 # number of points

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
		dict[(q,r)].append((x,y))
		if len(dict[(q,r)]) > nmax: 
			valid[i] = 0
	else:
		dict[(q,r)] = [(x,y)]

gal_weights = np.ones(npts)
for i in range(npts):
	x = gals[i,1]
	y = gals[i,2]
	q,r = crt2ax(x,y,hex_size)
	if len(dict[(q,r)]) > nmax:
		# change for weight as a column
		gal_weights[i] = len(dict[(q,r)])/np.float(nmax)

gals = np.insert(gals,5,gal_weights,1) # add gal weights as sixth column
gals = gals[valid==np.ones(npts)]
cols = np.array([1,2,3,5])
gals = gals[:,cols]
np.savetxt('../data/data_gals_2mil.txt',gals,delimiter=' ')



# to make unweighted
file = '../data/data_gals4.txt'
gals = np.loadtxt(file)
gal_weights = np.ones(gals.shape[0])
gals = np.insert(gals,4,gal_weights,1)
cols = np.array([0,1,2,4])
gals = gals[:,cols]
np.savetxt('../data/data_gals4b.txt',gals,delimiter=' ')

# scp bzg2@esca.astro.yale.edu:/home/bzg2/data/data_gals.txt .

observed_gals = gals[valid==np.ones(npts)] # do before gals[:,cols]
out_file = '../data/gal_locs_observed_' + str(npts/1000) + 'k.npy'
np.save(out_file, observed_gals)

