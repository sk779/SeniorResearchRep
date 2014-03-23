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
dfile = '../data/gals3'
pp <- ReadPairs(paste(dfile,"DD.dat",sep='-'))
norm <- ReadNorm(paste(dfile,"norm.dat",sep='-'))
Lbox <- 1000.0
density <- norm/(Lbox^3)

dd <- colSums(pp$pairs)
rlo <- pp$rbins[-length(pp$rbins)]
rhi <- pp$rbins[-1]

# These parameters define the logarithmic bins
rmin <- 0.3
rmax <- 200
nbins <- 200
logbins <- exp(seq(log(rmin),log(rmax),length.out=nbins))
ir <- cut(rlo, logbins, right=TRUE)

# Make data frame
df <- data.frame(ir=ir, rlo=rlo, rhi=rhi, dd=dd)
xi <- na.omit(ddply(df, .(ir), summarise, rmin=min(rlo), rmax=max(rhi), ddsum=sum(dd)))
xi$rrsum <- (4*pi/3)*((xi$rmax^3) - (xi$rmin^3))*density*norm
xi$xi <- xi$ddsum/xi$rrsum - 1
xi$r0 <- sqrt(xi$rmin*xi$rmax)


# set xi to appropriate variable
gg <- ggplot(upw, aes(x=r0, y=xi))
gg <- gg + geom_point() +  geom_point(data = dat, aes(y = xi), colour = 'green', size = 2)
gg <- gg + geom_point() +  geom_point(data = nupw, aes(y = xi), colour = 'red', size = 2)
gg <- gg + geom_point()+scale_x_log10()+scale_y_log10()
gg <- gg + xlab("r (Mpc/h)")  + ylab(expression(xi(r)))
#ggsave('../plots/gals4-xi.png', plot=gg)

# ratios
rdf=data.frame(r0=g4$r0,bl=dat$xi/dat$xi,comp1=upw$xi/dat$xi,comp2=nupw$xi/dat$xi)
gg <- ggplot(rdf, aes(x=r0, y=bl))
gg <- gg + geom_point() +  geom_point(data=rdf, aes(y = comp1), colour = 'green', size = 2)
gg <- gg + geom_point() +  geom_point(data=rdf, aes(y = comp2), colour = 'red', size = 2)
gg <- gg + xlab("r (Mpc/h)")  + ylab("Observed over Simulated Ratio")
ggsave('../plots/gals3-ratios.png', plot=gg)

