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

def getDists(gals,ngal):
	k=0
	nboxes = (1000/scale)**3
	if ngal==0: ngal=gals.shape[0]
	dists = np.zeros((ngal*ngal)/10.)
	weights = np.zeros((ngal*ngal)/10.)
	g = gals[0:ngal]
	for i in range(nboxes):
		if i%100==0: print i
		for j in range(nboxes):
			if isValidBox(i,j):
				pointsi = g[g[:,4]==i,:]
				pointsj = g[g[:,4]==j,:]
				for pi in pointsi:
					for pj in pointsj:
						d = dist(pi,pj)
						w = pi[5] * pj[5]
						if d<=150:
							dists[k] 	= d
							weights[k] 	= w
							k+=1
	dists = dists[dists!=0] #instead of np.trim_zeros(dists)
	weights = weights[dists!=0]
	# weights = weights[dists.argsort()]
	# dists = np.sort(dists)
	return dists, weights

def calcRR(r1,r2):
	univ_vol = 1000**3
	shell_vol = (4./3.)*(np.pi)*(r2**3 - r1**3)
	return (npts**2)*shell_vol/univ_vol

def calcTPCF(dn,rn):
	centers = np.zeros((nbins-1))
	tpcf = np.zeros((nbins-1))
	for i in range(0,nbins-1):
		r1 = bins[i]
		r2 = bins[i+1]
		centers[i] = (r1+r2)/2.
		RR = calcRR(r1,r2) #use for unobserved results?
		DD = dn[i]
		# RR = rn[i]
		try:
			tpcf[i] = np.float(DD)/RR - 1
		except ZeroDivisionError:
			tpcf[i] = 0
	return centers, tpcf

npts = 30000
scale = 100

dfile = '../data/gal_locs.npy'
dgals = np.load(dfile)
ddists, dweights = getDists(dgals,npts)

rfile = '../data/rand_gals.npy'
rgals = np.load(rfile)
rdists = getDists(rgals,npts)

nbins = 75
bins = np.logspace(np.log10(0.001),np.log10(150),nbins)
dn, bins = np.histogram(ddists, bins, weights=dweights)
rn, bins = np.histogram(rdists, bins)
centers, tpcfd = calcTPCF(dn,rn)
# centers, tpcf2 = calcTPCF(n2)

dat=np.array([tpcfo,tpcfow])
file='data/dist_hist_obs_30k.npy'
np.save(outfile,dat)

dat 	= np.load(file)
tpcfo 	= dat[0]
tpcfow	= dat[1]

# out_file = '../data/dists_observed_30k.npy'
# np.save(out_file, dn)
# out_file = '../data/rand_dists_observed_30k.npy'
# np.save(out_file, rn)

line1, = py.plot(centers,tpcfd,'bo')
line1l = py.plot(centers,tpcfd,'k')
# line2, = py.plot(centers,tpcf2,'ro')
# line2l = py.plot(centers,tpcf2,'k')

line1, = py.plot(centers,tpcfd,'bo')
line1l = py.plot(centers,tpcfd,'k')
line2, = py.plot(centers,tpcfo,'ro')
line2l, = py.plot(centers,tpcfo,'k')
line3, = py.plot(centers,tpcfow,'go')
line3l, = py.plot(centers,tpcfow,'k')
py.gca().set_xlabel('Distance Between Galaxies')
py.gca().set_ylabel(r'$\xi(r)$')
py.legend( (line1,line2,line3), ('Simulated Data','\"Observed\" Data', 'Observed with Weighting'), loc=2, numpoints=1 )
py.text(.015,.015,'npts = '+str(npts)+'\nhex_size = 8',bbox=dict(facecolor='none',alpha=1))
py.yscale('log'); py.xscale('log')
py.show()

line1, = py.plot(centers,tpcfd,'bo')
line1l = py.plot(centers,tpcfd,'k')
line3, = py.plot(centers,tpcfow,'go')
line3l, = py.plot(centers,tpcfow,'k')
py.gca().set_xlabel('Distance Between Galaxies')
py.gca().set_ylabel(r'Observed over Simulated TPCF')
py.legend( (line1,line3), ('Simulated Data','Observed with Weighting'), loc=3, numpoints=1 )
py.text(.0015,.0015,'npts = '+str(npts)+'\nhex_size = 8',bbox=dict(facecolor='none',alpha=1))
py.xscale('log')
py.show()

line1, = py.plot(centers,tpcf1*centers**2,'bo')
line1l = py.plot(centers,tpcf1*centers**2,'k')
# line2, = py.plot(centers,tpcf2*centers**2,'ro')
# line2l = py.plot(centers,tpcf2*centers**2,'k')
py.gca().set_xlabel('Distance Between Galaxies')
py.gca().set_ylabel(r'$r^2 \xi(r)$')
py.legend( (line1,line2), ('Simulated Data','\"Observed\" Data'), loc=6, numpoints=1 )
py.text(3,-6000,'npts = '+str(npts)+'\nhex_size = 8',bbox=dict(facecolor='none',alpha=1))
py.show()

