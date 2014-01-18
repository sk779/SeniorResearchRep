import numpy as np

def makeBoxes(scale):
	x = np.arange(0,1000,scale)
	y = np.arange(0,1000,scale)
	z = np.arange(0,1000,scale)
	boxes = np.zeros(((1000/scale)**3,3))
	count = 0
	for i in range(1000/scale):
		for j in range(1000/scale):
			for k in range(1000/scale):
				box = np.array([x[i],y[j],z[k]])
				boxes[count] = box
				count += 1
	return boxes

def dist(i,j):
	gali = gals[i]
	galj = gals[j]
	dk = np.array([0.,0.,0.])
	for k in range(3):
		d = abs(gali[k]-galj[k])
		if d>500: d = 1000-d
		dk[k] = d
	return np.sqrt(sum(dk**2))

def getDists(ngal, bid):
	k=0
	if ngal==0: ngal=gals.shape[0]
	dists = np.zeros((ngal*(ngal-1),3))
	for i in range(ngal):
		for j in range(ngal):
			if i!=j and boxes[i]==bid:
				d = dist(i,j) 
				if d<150.:
					dists[k] = np.array([d,boxes[i],boxes[j]])
					k+=1
	return dists

def isValidBox(b1,b2):
	i1 = b1/(1000/scale)**2; b1 -= i1*(1000/scale)**2
	j1 = b1/(1000/scale); b1 -= j1*(1000/scale)
	k1 = b1
	i2 = b2/(1000/scale)**2; b2 -= i2*(1000/scale)**2
	j2 = b2/(1000/scale); b2 -= j2*(1000/scale)
	k2 = b2
	di = abs(i1-i2)
	if di>500/scale:
		di = 1000/scale-di
	dj = abs(j1-j2)
	if dj>500/scale:
		dj = 1000/scale-dj
	dk = abs(k1-k2)
	if dk>500/scale:
		dk = 1000/scale-dk
	if di<2.1 and dj<2.1 and dk<2.1: 
		return True
	else:
		return False

gals = np.load('gal_locs.npy')
scale = 200
npts = 2000#gals.shape[0]
boxes = np.zeros(npts)
for i in range(npts):
	x = int(gals[i][0])
	y = int(gals[i][1])
	z = int(gals[i][2])
	boxes[i] = (x/scale)*(1000/scale)**2+(y/scale)*(1000/scale)+(z/scale)

dists = getDists(npts,0)
bs = np.unique(dists[:,2])