library(plyr)
library(ggplot2)

ReadPairs <- function (fn) {
  # Read in a pairs file, and fill in a list with useful information. This also rebins the data in r
  # Args :
  #   fn : filename
  # Outputs :
  #     pairs : array (nmu, nr) of pair counts
  
  ff <- gzfile(fn, "r")
  # Read in rbins
  rbins <- scan(ff,numeric(0),nlines=1)
  nrbins <- length(rbins)-1
  mubins <- scan(ff, numeric(0),nlines=1)
  nmubins <- length(mubins)-1
  pairs <- array(scan(ff, numeric(0)), c(nmubins, nrbins))
  close(ff)
  list(rbins=rbins, mubins=mubins, pairs=pairs)
}

ReadNorm <- function(fn) {
  # Read in the norm file
  read.table(fn)[,2]
}

Compute2DXi <- function(DD,DR,RR,norm) {
  rcen <- DD$rcen
  rbins <- DD$rbins
  mubins <- DD$mubins
  r0 <- (head(rbins,-1)+tail(rbins,-1))/2
  mu0 <- (head(mubins,-1)+tail(mubins,-1))/2
  dmu <- diff(mubins,1)
#   fac <- norm[1]/norm[2]
#   rhi=rbins[-1]
#   rlo=rbins[-length(DD$rbins)]
  rmin <- 0.01
  rmax <- 200
  nbins <- 200
  logbins <- exp(seq(log(rmin),log(rmax),length.out=nbins+1))
  rhi=logbins[-1]
  rlo=logbins[-length(DD$rbins)]

#   ir <- cut(rlo, logbins, right=TRUE)
#   df <- data.frame(ir=ir, rlo=rlo, rhi=rhi)
#   lbins <- na.omit(ddply(df, .(ir), summarise, rmin=min(rlo), rmax=max(rhi)))
  RR = (2*pi)*outer(dmu,(rhi^3-rlo^3))*density*norm
  xi <- (DD$pairs/RR)-1
#   xi <- (DD$pairs - 2*DR$pairs*fac + RR$pairs*(fac^2))/(RR$pairs*(fac^2))
  list(r0=r0, mu0=mu0, dmu=dmu,rcen=rcen, xi=xi)
}

# Define the Legendre polynomials
L2 <- function(mu) {
  (3*mu^2-1)/2
}
L4 <- function(mu) {
  (3-30*mu^2+35*mu^4)/8
}

ComputeMultipoles <- function(xi2d) {
  l2 <- L2(xi2d$mu0)*xi2d$dmu
#   l4 <- L4(xi2d$mu0)*xi2d$dmu
  xi0 <- colSums(xi2d$xi*xi2d$dmu)
  xi2 <- colSums(xi2d$xi*l2)*5
#   xi4 <- colSums(xi2d$xi*l4)*9
  data.frame("r0"=xi2d$r0, "xi0"=xi0, "xi2"=xi2)
}

setwd('/Users/Ben/Documents/Yale/Senior Year/Spring 2014/Physics 472 Independent Projects in Physics/SeniorResearchRep')
dfile = '../data/gals_vz_correction_2mil'
pp <- ReadPairs(paste(dfile,"DD.dat",sep='-'))
# pq <- ReadPairs(paste(dfile,"DR.dat",sep='-'))
# qq <- ReadPairs(paste(dfile,"RR.dat",sep='-'))
norm <- ReadNorm(paste(dfile,"norm.dat",sep='-'))
norm = norm[1]
Lbox <- 1000.0
density <- norm[1]/(Lbox^3)

xi2d = Compute2DXi(pp,pq,qq,norm)
dat = ComputeMultipoles(xi2d)
dat = dat[1:125,]

# plotting 
gg <- ggplot(dat, aes(x=r0, y=abs(dat$r0^2*xi0))) + geom_text(aes(x=30,y=20,label='Monopole'),colour='black',size=7)
gg <- gg + geom_point() + geom_point(data = dat, aes(y = abs(dat$r0^2*xi2)), colour = 'blue', size = 2) + geom_text(aes(x=30,y=16,label='Quadrupole'),colour='blue',size=7)
# gg <- gg + geom_point() + geom_point(data = dat, aes(y = abs(dat$r0^2*xi4)), colour = 'red', size = 2)
gg <- gg + geom_point()# + scale_x_log10() + scale_y_log10()
gg <- gg + xlab("r (Mpc/h)")  + ylab(expression(abs(r^2*xi(r))))
gg <- gg + theme(axis.title=element_text(face="bold", size=20), axis.text=element_text(face="bold", size=20))
gg <- gg + annotate('text',x=30,y=10,label='2 million galaxies')
# ggsave('../plots/multipoles_test_r2xi.png', plot=gg)
