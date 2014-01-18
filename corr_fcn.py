import matplotlib.pyplot as plt
import numpy as np
import pylab as py
from boxes_test import isValidBox

def dist(pi,pj):
	# gali = gals[i]
	# galj = gals[j]
	dk = np.array([0.,0.,0.])
	for k in range(1,4):
		# d = abs(gali[k]-galj[k])
		d = abs(pi[k]-pj[k])
		if d>500: d = 1000-d
		dk[k-1] = d
	return np.sqrt(sum(dk**2))

def getDists(ngal):
	k=0
	nboxes = (1000/scale)**3
	if ngal==0: ngal=gals.shape[0]
	dists = np.zeros((ngal*ngal)/10.)
	g = gals[0:ngal]
	for i in range(nboxes):
		if i%250==0: print i
		for j in range(nboxes):
			if isValidBox(i,j):
				pointsi = g[g[:,4]==i,:]
				pointsj = g[g[:,4]==j,:]
				for pi in pointsi:
					for pj in pointsj:
						d = dist(pi,pj)
						if d<=150:
							dists[k] = d
							k+=1
	dists = np.trim_zeros(np.sort(np.trim_zeros(dists)))
	return dists

def calcRR(r1,r2):
	univ_vol = 1000**3
	shell_vol = (4./3.)*(np.pi)*(r2**3 - r1**3)
	return (npts**2)*shell_vol/univ_vol

def calcTPCF(n):
	centers = np.zeros((nbins-1))
	tpcf = np.zeros((nbins-1))
	for i in range(0,nbins-1):
		r1 = bins[i]
		r2 = bins[i+1]
		centers[i] = (r1+r2)/2.
		RR = calcRR(r1,r2)
		DD = n[i]
		tpcf[i] = DD/RR - 1
	return centers, tpcf

in_file = 'gal_locs.npy'
gals = np.load(in_file)
npts = 30000
scale = 100

dists = getDists(npts)
out_file = 'dists_pruned_30k.npy'
np.save(out_file, dists)

nbins = 75
bins = np.logspace(np.log10(0.001),np.log10(150),nbins)
n1, bins = np.histogram(dists1, bins)
n2, bins = np.histogram(dists2, bins)
centers, tpcf1 = calcTPCF(n1)
centers, tpcf2 = calcTPCF(n2)


line1, = py.plot(centers,tpcf1,'bo')
line1l = py.plot(centers,tpcf1,'k')
line2, = py.plot(centers,tpcf2,'ro')
line2l = py.plot(centers,tpcf2,'k')
py.gca().set_xlabel('Distance Between Galaxies')
py.gca().set_ylabel(r'$\xi(r)$')
py.legend( (line1,line2), ('Simulated Data','\"Observed\" Data'), loc=6, numpoints=1 )
py.text(.0015,.0015,'npts = '+str(npts)+'\nhex_size = 8',bbox=dict(facecolor='none',alpha=1))
py.yscale('log'); py.xscale('log')
py.show()


line1, = py.plot(centers,tpcf1*centers**2,'bo')
line1l = py.plot(centers,tpcf1*centers**2,'k')
line2, = py.plot(centers,tpcf2*centers**2,'ro')
line2l = py.plot(centers,tpcf2*centers**2,'k')
py.gca().set_xlabel('Distance Between Galaxies')
py.gca().set_ylabel(r'$r^2 \xi(r)$')
py.legend( (line1,line2), ('Simulated Data','\"Observed\" Data'), loc=6, numpoints=1 )
py.text(3,-6000,'npts = '+str(npts)+'\nhex_size = 8',bbox=dict(facecolor='none',alpha=1))
py.show()

