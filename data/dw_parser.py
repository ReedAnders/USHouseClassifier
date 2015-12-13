dwRaw = open('DW Individual.dat','r')

dwList = dwRaw.readlines()

billName = {}

for ii in dwList:
	ll = ii.split()

	if ll[0] != '113':
		continue

	if ll[0] == '113':
		if ll[6] == 'GRAVES':
			import pdb; pdb.set_trace()


import pdb; pdb.set_trace()