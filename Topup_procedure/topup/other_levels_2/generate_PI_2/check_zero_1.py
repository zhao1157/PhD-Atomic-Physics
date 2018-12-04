#This script is to remove the first point that is zero.
import os

ind_low = 1
ind_hig = 123 

os.popen('if [ -d xsectn_clean ]; then rm -rf xsectn_clean; fi; mkdir xsectn_clean')
for i in range(ind_low, 1+ind_hig):
	f_write = open('xsectn_clean/'+str(i), 'w')
	for line in open('xsectn/'+str(i)):
		data = float(line.split()[1])
		if data == 0:
			print (i)
		else: 
			f_write.write(line)	
