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

# Process the pairs file 
# Here, we assume that this is generated assuming purely periodic boundary conditions
# Therefore RR is completely isotropic and can be analytically estimated. 
setwd('/Users/Ben/Documents/Yale/Senior Year/Spring 2014/Physics 472 Independent Projects in Physics/SeniorResearchRep')
dfile = '../data/gals_2mil_hs4_withrands'
pp <- ReadPairs(paste(dfile,"DD.dat",sep='-'))
# pq <- ReadPairs(paste(dfile,"DR.dat",sep='-'))
# qq <- ReadPairs(paste(dfile,"RR.dat",sep='-'))
norm <- ReadNorm(paste(dfile,"norm.dat",sep='-'))
Lbox <- 1000.0
density <- norm/(Lbox^3)
# Nd=norm[1]
# Nr=norm[2]
# ddnorm=Nd*Nd/2
# rrnorm=Nr*(Nr-1)/2
# drnorm=Nd*Nr

dd <- colSums(pp$pairs)
# dr <- colSums(pq$pairs)
# rr <- colSums(qq$pairs)
rlo <- pp$rbins[-length(pp$rbins)]
rhi <- pp$rbins[-1]

# These parameters define the logarithmic bins
rmin <- 0.3
rmax <- 200
nbins <- 200
logbins <- exp(seq(log(rmin),log(rmax),length.out=nbins))
ir <- cut(rlo, logbins, right=TRUE)

# Make data frame
df <- data.frame(ir=ir, rlo=rlo, rhi=rhi, dd=dd)#,dr=dr,rr=rr)
xi <- na.omit(ddply(df, .(ir), summarise, rmin=min(rlo), rmax=max(rhi), ddsum=sum(dd)))#,drsum=sum(dr),rrsum=sum(rr)))
xi$rrsum <- (4*pi/3)*((xi$rmax^3) - (xi$rmin^3))*density*norm
xi$xi <- xi$ddsum/xi$rrsum - 1
# xi$xi <- (xi$ddsum-2*xi$drsum+xi$rrsum)/xi$rrsum
xi$r0 <- sqrt(xi$rmin*xi$rmax)


# set xi to appropriate variable: dat, upw, nupw = xi
gg <- ggplot(dat, aes(x=r0, y=xi))
gg <- gg + geom_point() + geom_point(data = upw, aes(y = xi), colour = 'blue', size = 2)
gg <- gg + geom_point() + geom_point(data = nupw, aes(y = xi), colour = 'red', size = 2)
gg <- gg + geom_point() + scale_x_log10() + scale_y_log10()
gg <- gg + xlab("r (Mpc/h)")  + ylab(expression(xi(r)))
# ggsave('../plots/gals_2mil_nm4-xi.png', plot=gg)

# ratios
rdf=data.frame(r0=upw$r0,bl=dat$xi/dat$xi,comp1=upw$xi/dat$xi,comp2=nupw$xi/dat$xi)
gg <- ggplot(rdf, aes(x=r0, y=bl))
gg <- gg + geom_point() +  geom_point(data=rdf, aes(y = comp1), colour = 'blue', size = 2)
gg <- gg + geom_point() +  geom_point(data=rdf, aes(y = comp2), colour = 'red', size = 2)
gg <- gg + xlab("r (Mpc/h)")  + ylab("Observed over Simulated Ratio")
# ggsave('../plots/gals_2mil_nm4-ratios.png', plot=gg)

# comparison
# corr fcn rdf=data.frame(r0=upw$r0,bl=dat$xi,comp1=three$xi,comp2=four$xi,comp3=five$xi)
# ratios rdf=data.frame(r0=upw$r0,bl=dat$xi/dat$xi,comp1=three$xi/dat$xi,comp2=four$xi/dat$xi,comp3=five$xi/dat$xi)
gg <- ggplot(rdf, aes(x=r0, y=bl))
gg <- gg + geom_point() +  geom_point(data=rdf, aes(y = comp1), colour = 'blue', size = 2)
gg <- gg + geom_point() +  geom_point(data=rdf, aes(y = comp2), colour = 'red', size = 2)
gg <- gg + geom_point() +  geom_point(data=rdf, aes(y = comp3), colour = 'green', size = 2)
# gg <- gg + geom_point() + scale_x_log10() + scale_y_log10() #corr fcn
gg <- gg + xlab("r (Mpc/h)")  + ylab("Observed over Simulated Ratio")
# ggsave('../plots/gals_2mil-nmcomp.png', plot=gg)
