#! This script is to combine the head and xsectn
import os
#set the target charge
charge_target = 17
#set the base index
ind_base = 464
#set the index range of the file
ind_low = 1	#This should be 1, or else the following code might be wrong.
ind_hig = 123 

f_write = open('xsectn_combine', 'w')
f_levels = open('levels')
for i in range(ind_low, ind_hig+1):
	for line in open('head'): f_write.write(line)
	f_write.write('    0 {0:8d}    0    1\n'.format(ind_base+i))
	en=charge_target*charge_target*float(f_levels.readline().split()[2])
	num_xsectn = int(os.popen('wc -l xsectn_clean/'+str(i)).read().split()[0]) 
	f_write.write('{0:15.6E}     {1:d}\n'.format(en, num_xsectn))
	f_write.write('    0.000000\n')
	
	count = 0
	for line in open('xsectn_clean/'+str(i)):
		count += 1
		f_write.write(line)
	if count != num_xsectn:
		print ('error')
		raise SystemExit
