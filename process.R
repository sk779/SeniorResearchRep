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
dfile = '../data/gals3b'#_2mil_hs3'
pp <- ReadPairs(paste(dfile,"DD.dat",sep='-'))
norm <- ReadNorm(paste(dfile,"norm.dat",sep='-'))
Lbox <- 1000.0
density <- norm/(Lbox^3)

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
xi$r0 <- sqrt(xi$rmin*xi$rmax)


# set xi to appropriate variable: dat, upw, nupw = xi
gg <- ggplot(dat, aes(x=r0, y=xi)) + geom_text(aes(x=55,y=3,label='Data'),colour='black',size=7)
gg <- gg + geom_point() + geom_point(data = upw, aes(y = xi), colour = 'blue', size = 2) + geom_text(aes(x=55,y=1.6,label='Observed With Upweighting'),colour='blue',size=7)
gg <- gg + geom_point() + geom_point(data = nupw, aes(y = xi), colour = 'red', size = 2) + geom_text(aes(x=55,y=0.9,label='Observed Without Correction'),colour='red',size=7)
gg <- gg + geom_point() + scale_x_log10() + scale_y_log10()
gg <- gg + xlab("r (Mpc/h)")  + ylab(expression(xi(r)))
gg <- gg + annotate('text',x=2,y=.03,label='2 million points\nnmax=5\nhex_size=1Mpc')

# ggsave('../plots/gals_2mil_correction-xi.png', plot=gg)

# ratios
rdf=data.frame(r0=upw$r0,bl=dat$xi/dat$xi,comp1=upw$xi/dat$xi,comp2=nupw$xi/dat$xi)
rdf=rdf[1:74,]
gg <- ggplot(rdf, aes(x=r0, y=bl)) + geom_text(aes(x=25,y=.635,label='Data'),colour='black',size=7)
gg <- gg + geom_line() +  geom_line(data=rdf, aes(y = comp1), colour = 'blue', size = 1) + geom_text(aes(x=25,y=.6,label='Observed With Upweighting'),colour='blue',size=7)
gg <- gg + geom_point() +  geom_line(data=rdf, aes(y = comp2), colour = 'red', size = 1) + geom_text(aes(x=25,y=.565,label='Observed Without Correction'),colour='red',size=7)
gg <- gg + xlab("r (Mpc/h)")  + ylab("Observed over Simulated Ratio")
gg <- gg + annotate('text',x=12.5,y=.75,label='2 million points\nnmax=5\nhex_size=1Mpc')
# ggsave('../plots/gals_2mil_correction-ratios.png', plot=gg)

# comparison
# corr fcn rdf=data.frame(r0=upw$r0,bl=dat$xi,comp1=three$xi,comp2=four$xi,comp3=five$xi)
# ratios rdf=data.frame(r0=upw$r0,bl=dat$xi/dat$xi,comp1=three$xi/dat$xi,comp2=four$xi/dat$xi,comp3=five$xi/dat$xi)
gg <- ggplot(rdf, aes(x=r0, y=bl)) + geom_text(aes(x=37.5,y=1.1,label='Data'),colour='black',size=7)
gg <- gg + geom_line() +  geom_line(data=rdf, aes(y = comp1), colour = 'blue', size = 1) + geom_text(aes(x=37.5,y=1.085,label='nmax=3'),colour='blue',size=7)
gg <- gg + geom_point() +  geom_line(data=rdf, aes(y = comp2), colour = 'red', size = 1) + geom_text(aes(x=37.5,y=1.07,label='nmax=4'),colour='red',size=7)
gg <- gg + geom_point() +  geom_line(data=rdf, aes(y = comp3), colour = 'green4', size = 1) + geom_text(aes(x=37.5,y=1.055,label='nmax=5'),colour='green4',size=7)
# gg <- gg + geom_point() + scale_x_log10() + scale_y_log10() #corr fcn
gg <- gg + xlab("r (Mpc/h)")  + ylab("Observed over Simulated Ratio")
# ggsave('../plots/gals_2mil_nm4_weighting-comp-ratios.png', plot=gg)
