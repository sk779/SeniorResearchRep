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
pp <- ReadPairs("t1-DD.dat")
norm <- ReadNorm("t1-norm.dat")
Lbox <- 1000.0
density <- norm/(Lbox^3)

dd <- colSums(pp$pairs)
rlo <- pp$rbins[-length(pp$rbins)]
rhi <- pp$rbins[-1]

# These parameters define the logarithmic bins
rmin <- 0.3
rmax <- 75.0
nbins <- 15
logbins <- exp(seq(log(rmin),log(rmax),length.out=nbins))
ir <- cut(rlo, logbins, right=TRUE)

# Make data frame
df <- data.frame(ir=ir, rlo=rlo, rhi=rhi, dd=dd)
xi <- na.omit(ddply(df, .(ir), summarise, rmin=min(rlo), rmax=max(rhi), ddsum=sum(dd)))
xi$rrsum <- (4*pi/3)*((xi$rmax^3) - (xi$rmin^3))*density*norm
xi$xi <- xi$ddsum/xi$rrsum - 1
xi$r0 <- sqrt(xi$rmin*xi$rmax)

gg <- ggplot(xi, aes(x=r0, y=xi))
gg <- gg + geom_point()+scale_x_log10()+scale_y_log10()
gg <- gg + xlab("r (Mpc/h)")  + ylab(expression(xi(r)))
ggsave("t1-xi.png", plot=gg)
