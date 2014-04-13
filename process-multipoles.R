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
  fac <- norm[1]/norm[2]
  xi <- (DD$pairs - 2*DR$pairs*fac + RR$pairs*(fac^2))/(RR$pairs*(fac^2))
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
  l4 <- L4(xi2d$mu0)*xi2d$dmu
  xi0 <- colSums(xi2d$xi*xi2d$dmu)
  xi2 <- colSums(xi2d$xi*l2)*5
  xi4 <- colSums(xi2d$xi*l4)*9
  data.frame("r0"=xi2d$r0, "xi0"=xi0, "xi2"=xi2, "xi4"=xi4)
}

setwd('/Users/Ben/Documents/Yale/Senior Year/Spring 2014/Physics 472 Independent Projects in Physics/SeniorResearchRep')
dfile = '../data/gals_2mil_hs4_withrands'
pp <- ReadPairs(paste(dfile,"DD.dat",sep='-'))
pq <- ReadPairs(paste(dfile,"DR.dat",sep='-'))
qq <- ReadPairs(paste(dfile,"RR.dat",sep='-'))
norm <- ReadNorm(paste(dfile,"norm.dat",sep='-'))

xi2d = Compute2DXi(pp,pq,qq,norm)
dat = ComputeMultipoles(xi2d)

# plotting 
gg <- ggplot(dat, aes(x=r0, y=xi0))
gg <- gg + geom_point() + geom_point(data = dat, aes(y = xi2), colour = 'blue', size = 2)
gg <- gg + geom_point() + geom_point(data = dat, aes(y = xi4), colour = 'red', size = 2)
gg <- gg + geom_point() + scale_x_log10() + scale_y_log10()
gg <- gg + xlab("r (Mpc/h)")  + ylab(expression(xi(r)))
# ggsave('../plots/_gals_2mil_nm4-xi.png', plot=gg)
