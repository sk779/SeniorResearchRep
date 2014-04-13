ReadPairs <- function (fn, skip=0, rebin=1) {
  # Read in a pairs file, and fill in a list with useful information. This also rebins the data in r
  # Args :
  #   fn : filename
  #   skip : initial bins to skip
  #   rebin : rebin size 
  # Outputs :
  #   list with the following elements
  #     rbins : r bin boundaries
  #     nr    : number of r bins (length(rbins)-1)
  #     mubins : mu bin boundaries
  #     nmu : number of mu bins
  #     pairs : array (nmu, nr) of pair counts
  #     rcen : central r values weighted by number of pairs
  
  ff <- file(fn, "r")
  # Read in rbins
  rbins <- scan(ff,numeric(0),nlines=1)
  nrbins <- length(rbins)-1
  mubins <- scan(ff, numeric(0),nlines=1)
  nmubins <- length(mubins)-1
  pairs <- array(scan(ff, numeric(0)), c(nmubins, nrbins))
  close(ff)
    
  # Since we will be rebinning in r, useful to compute mean weighted r
  rweight <- apply(pairs, 2, sum)
  rcen <- (rbins[1:nrbins]+rbins[2:(nrbins+1)])*rweight/2
  
  # Now we want to skip and rebin the data
  # rbins
  s1 <- seq(skip+1, nrbins+1, rebin)
  rbins <- rbins[s1]
  nrbins <- length(rbins)-1
  
  # rcen
  elts <- (skip+1):(skip+rebin*nrbins)
  rcen <- colSums(array(rcen[elts],c(rebin,nrbins))) 
  rweight <- colSums(array(rweight[elts],c(rebin,nrbins)))
  pairs <- apply(array(pairs[,elts],c(nmubins, rebin, nrbins)), c(1,3), sum)
  
  list(rbins=rbins, nr=nrbins, mubins=mubins, nmu=nmubins, pairs=pairs, rcen=rcen/rweight)
}

ReadNorm <- function(fn) {
  # Read in the norm file
  read.table(fn)[,2]
}

ReadSet <- function(fnprefix, RRn.prefix, RRd.prefix, ...) {
  # Read in a full set of paircounts. We handle the RR terms separately, since these 
  # are not always in the same set. Returns a list with DD,DR, RRn (RR in the numerator), and RRd (denominator)
  dd <- ReadPairs(paste(fnprefix,'-DD.dat',sep=""),...)
  dr <- ReadPairs(paste(fnprefix,'-DR.dat',sep=""),...)
  norm <- ReadNorm(paste(fnprefix,'-norm.dat',sep=""))
  rrn <- ReadPairs(paste(RRn.prefix,'-RR.dat',sep=""),...)
  norm1 <- ReadNorm(paste(RRn.prefix,'-norm.dat',sep=""))
  stopifnot((norm1[2]-norm[2])/norm[2] < 1.e-8)
  rrd <- ReadPairs(paste(RRd.prefix,'-RR.dat',sep=""),...)
  norm1 <- ReadNorm(paste(RRd.prefix,'-norm.dat',sep=""))
  stopifnot((norm1[2]-norm[2])/norm[2] < 1.e-8)
  list(DD=dd, DR=dr, RRn=rrn, RRd=rrd, norm=norm)
} 

AddPairs <- function(p1, p2) {
  # Simply add the pairs and the norms
  # Useful in adding North and South
  psum <- p1
  psum$DD$pairs <- p1$DD$pairs +  p2$DD$pairs
  psum$DR$pairs <- p1$DR$pairs +  p2$DR$pairs
  psum$RRn$pairs <- p1$RRn$pairs +  p2$RRn$pairs
  psum$RRd$pairs <- p1$RRd$pairs +  p2$RRd$pairs
  psum$norm <- p1$norm + p2$norm
  psum
}


Compute2DXi <- function(pairlist) {
  rcen <- pairlist$DD$rcen
  rbins <- pairlist$DD$rbins
  mubins <- pairlist$DD$mubins
  r0 <- (head(rbins,-1)+tail(rbins,-1))/2
  mu0 <- (head(mubins,-1)+tail(mubins,-1))/2
  dmu <- diff(mubins,1)
  fac <- pairlist$norm[1]/pairlist$norm[2]
  xi <- (pairlist$DD$pairs - 2*pairlist$DR$pairs*fac + pairlist$RRn$pairs*(fac^2))/(pairlist$RRd$pairs*(fac^2))
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
  
  data.frame("r0"=xi2d$r0,"rcen"=xi2d$rcen, "xi0"=xi0, "xi2"=xi2, "xi4"=xi4)
}


