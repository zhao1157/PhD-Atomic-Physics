file_name = 'fe19_ss.en'

keys = [str(i) for i in range(1, 13)] #configuration index as in superstructure
values = [0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0] #parity of the configuration in the order
											   #of the input in superstructure.
cf_p = dict(zip(keys, values))

f = open('core_lsp', 'w')
for line in open(file_name):
	l_spt = line.split()
	l_spt[3] = int(l_spt[3])
	
	#the first two conditions are just to check
	if l_spt[3]>0 and cf_p[l_spt[5]]==0:
		pass
	elif l_spt[3]<0 and cf_p[l_spt[5]]==1:
		pass
	else:
		print ('configuration and parity mismatch.')
	
	f.write('{0:>3s}{1:3d}{2:3d}\n'.format(l_spt[4], abs(l_spt[3]), cf_p[l_spt[5]]))
	
	
	
	
	
	
