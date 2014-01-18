import random
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()

fig, ax = plt.subplots()
patches = []
size=5
n=20
bound=20

gals = np.load('gal_locs.npy')

npts=2000
for i in range(npts):
    x = gals[i][1]
    y = gals[i][2]
    plt.plot(x,y,'bo')

plt.show()
