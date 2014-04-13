import math

# using a pointy-top hexagon arrangement

# estimate axial coordinates based on x, y
def approxAx(x,y,s):
	q = ((math.sqrt(3.)/3.)*x-y/3.)/s
	r = (2./3.)*(y/s)
	return q, r

# convert from axial to cube coordinates
def ax2cb(q,r):
	x = q
	z = r
	y = -x-z
	return x, y, z

# determine the hexagon index based on cube coordinates
def hexRound(x,y,z):
	rx = round(x)
	ry = round(y)
	rz = round(z)
	if (rx+ry+rz)==0:
		return int(rx), int(ry), int(rz)
	else:
		x_err = math.fabs(rx-x)
		y_err = math.fabs(ry-y)
		z_err = math.fabs(rz-z)
		if x_err>y_err and x_err>z_err:
			rx = -ry-rz
		elif y_err>z_err:
			ry = -rx-rz
		else:
			rz = -rx-ry
		return int(rx), int(ry), int(rz)

# convert from cube to axial coordinates
def cb2ax(x,y,z):
	q = x
	r = z
	return q, r

# convert from axial to x-y coordinates
def drawConvert(q,r,s):
	x = s * math.sqrt(3) * (q + .5*r)
	y = s * (3./2.) * r
	return [x,y]

# convert from cartesian to axial coordinates
def crt2ax(x,y,s):
    q,r = approxAx(x, y, s)
    x,y,z = ax2cb(q,r)
    x,y,z = hexRound(x,y,z)
    return cb2ax(x,y,z)

