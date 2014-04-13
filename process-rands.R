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

setwd('/Users/Ben/Documents/Yale/Senior Year/Spring 2014/Physics 472 Independent Projects in Physics/SeniorResearchRep')
dfile = '../data/gals_2mil_hs4_withrands'
pp <- ReadPairs(paste(dfile,"DD.dat",sep='-'))
pq <- ReadPairs(paste(dfile,"DR.dat",sep='-'))
qq <- ReadPairs(paste(dfile,"RR.dat",sep='-'))
norm <- ReadNorm(paste(dfile,"norm.dat",sep='-'))
Lbox <- 1000.0
density <- norm/(Lbox^3)

Nd=norm[1]
Nr=norm[2]
ddnorm=Nd*Nd
rrnorm=Nr*Nr
drnorm=Nd*Nr

dd <- colSums(pp$pairs)
dr <- colSums(pq$pairs)
rr <- colSums(qq$pairs)
rlo <- pp$rbins[-length(pp$rbins)]
rhi <- pp$rbins[-1]

# These parameters define the logarithmic bins
rmin <- 0.3
rmax <- 200
nbins <- 200
logbins <- exp(seq(log(rmin),log(rmax),length.out=nbins))
ir <- cut(rlo, logbins, right=TRUE)

# Make data frame
df <- data.frame(ir=ir, rlo=rlo, rhi=rhi, dd=dd, dr=dr, rr=rr)
xi <- na.omit(ddply(df, .(ir), summarise, rmin=min(rlo), rmax=max(rhi), ddsum=sum(dd)/ddnorm,drsum=sum(dr)/drnorm,rrsum=sum(rr)/rrnorm))
xi$xi <- (xi$ddsum-2*xi$drsum+xi$rrsum)/xi$rrsum
xi$r0 <- sqrt(xi$rmin*xi$rmax)


# set xi to appropriate variable: dat, upw, nupw = xi
gg <- ggplot(dat, aes(x=r0, y=xi))
gg <- gg + geom_point() + geom_point(data = upw, aes(y = xi), colour = 'blue', size = 2)
gg <- gg + geom_point() + geom_point(data = nupw, aes(y = xi), colour = 'red', size = 2)
gg <- gg + geom_point() + scale_x_log10() + scale_y_log10()
gg <- gg + xlab("r (Mpc/h)")  + ylab(expression(xi(r)))
# ggsave('../plots/gals_2mil_nm4-xi.png', plot=gg)
