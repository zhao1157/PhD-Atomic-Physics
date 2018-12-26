#This script is to extract the photoionization cross section at the end of the main transition and at 500 Ry

import os
#Set the path to the n_start_end drectory
n_start_end = 'n_start_end'
#Set the path to store the photoionization cross section
pi_end_500 = 'pi_end_500'
#Set the path to photoionization cross section
dir_pi = '../generate_PI_2/xsectn'


#======= BLACK BOX =========
os.popen('if [ -d '+pi_end_500+' ]; then rm -rf '+pi_end_500+';fi; mkdir '+pi_end_500+';')
for n_elec in range(2, 11):
	f_write = open(pi_end_500+'/'+str(n_elec), 'w')
	for line in open(n_start_end+'/'+str(n_elec)):
		ind, start, end = line.split()
		end = float(end)
		num_line = int(os.popen('wc -l '+dir_pi+'/'+ind).read().split()[0])
		
		f_read = open(dir_pi+'/'+ind)
		count = 0
		for i in range(num_line):
			en, pi = f_read.readline().split()
			if end <= float(en):
				count += 1
				pi_end = pi
				if count == 2: 
					break
		for j in range(i+1, num_line):
			en, pi = f_read.readline().split()
			if 500 <= float(en):
				pi_500 = pi
		f_write.write('{0} {1}\n'.format(pi_end, pi_500))
