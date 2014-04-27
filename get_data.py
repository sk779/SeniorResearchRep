import numpy as np
import csv
import paramiko as pm

def getFile(in_file):
ssh = pm.SSHClient()
ssh.set_missing_host_key_policy(pm.AutoAddPolicy())
ssh.connect('esca.astro.yale.edu',username='----',password='------')
ftp = ssh.open_sftp()
ftp.get(in_file, in_file) 
ftp.close()
ssh.close()

# def getBox(x,y,z,scale):
# 	box = (int(x)/scale)*(1000/scale)**2+(int(y)/scale)*(1000/scale)+(int(z)/scale)
# 	return(box)

def getCoords(in_file, out_file):
	reader = csv.reader(open(in_file))
	# writer = csv.writer(open(out_file,'w'))
	# dt = np.dtype([ ('rand', 'd'), ('x', 'd'), ('y', 'd'), ('z', 'd'), ('box', 'i') ])
	gals = np.zeros([3845257,5])
	rn = 0
	for row in reader:
		if len(row)>10:
			try:
				x = float(row[4])
				y = float(row[5])
				z = float(row[6])
				vz = float(row[9])/100.
				zpvz = z+vz
				# box = getBox(x,y,z,scale)
				# writer.writerow([np.random.uniform(),x,y,z,box,'\n'])
				gals[rn] = np.array([np.random.uniform(),x,y,z,zpvz])
				rn = rn+1
			except ValueError:
				print 'row headers'
	gals = gals[gals[:,0].argsort()]
	np.save(out_file, gals)

scale = 100
in_file = 'MultiDark_z_0_Vcir_200_M_12.txt'
out_file = 'data/gal_locs_vz_correction.npy'
getCoords(in_file,out_file)