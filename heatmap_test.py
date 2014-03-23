#import numpy as np
#import numpy.random
#import matplotlib.pyplot as plt
#
## Generate some test data
#x = np.random.randn(8873)
#y = np.random.randn(8873)
#
#heatmap, xedges, yedges = np.histogram2d(x, y, bins=10)
#extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
#
#plt.clf()
#plt.imshow(heatmap, extent=extent)
#plt.show()


from matplotlib import pyplot as PLT
from matplotlib import cm as CM
from matplotlib import mlab as ML
import numpy as NP

#x = y = NP.linspace(-5, 5, 100)
#print y
#X, Y = NP.meshgrid(x, y)
#print X
#Z1 = ML.bivariate_normal(X, Y, 2, 2, 0, 0)
#print Z1
#Z2 = ML.bivariate_normal(X, Y, 4, 1, 1, 1)
#ZD = Z2 - Z1
#x = X.ravel()
#print x
#y = Y.ravel()
#z = ZD.ravel()
#gridsize=30
#PLT.subplot(111)

x = [1,2,3]
y = [1,2,3]
z = [10,20,30]
gridsize = 20

# if 'bins=None', then color of each hexagon corresponds directly to its count
# 'C' is optional--it maps values to x-y coordinates; if 'C' is None (default) then
# the result is a pure 2D histogram

PLT.hexbin(x, y, C=z, gridsize=gridsize, cmap=CM.jet, bins=None)
PLT.axis([0, 5, 0, 5])

cb = PLT.colorbar()
cb.set_label('mean value')
PLT.show()