#This script is to print out the start and end of the main transitions

import os

#set the exponet of the photoionization cross section
exp_pi = ['+02', '+01', '+00']
#Set the directory where to read the output files
read_file = 'outfile'
#Set the directory to store the n_start_end information
file_n_start_end = 'n_start_end'
#Set the path to the file containing the bound levels
file_bound = '../bound_levels_0/neg'

##=========== BLACK BOX ==========
#Read the bound levels and the principle quantum number of the outer electron
bound_levels = []
for line in open(file_bound):
        bound_levels.append(line.split()[0]+'_'+line.split()[1])

os.popen('if [ -d '+file_n_start_end+' ]; then rm -rf '+file_n_start_end+';fi; mkdir '+file_n_start_end+';')

collect_n_start_end = {}

ind = 0 #line number, which is the same as the name of the photoionization cross section file in generate_PI_2/xsectn
for lev_n in bound_levels:
	ind += 1
	lev, n_elec = lev_n.split('_')
	en_ion = []
	if not n_elec in collect_n_start_end:
		collect_n_start_end[n_elec] = []	
	for exp in exp_pi:
		if os.path.isfile(read_file+'/'+lev+'_'+exp):
			f_read = open(read_file+'/'+lev+'_'+exp)
			num_line = int(os.popen('wc -l '+read_file+'/'+lev+'_'+exp).read().split()[0])
			for i in range(num_line/7):
				line = f_read.readline()
				en_ion.append(float(line.split()[4]))
				for j in range(6): f_read.readline()
	if len(en_ion) == 0:
		print ('level {0} small'.format(lev_n))
		continue
	collect_n_start_end[n_elec].append({})
	collect_n_start_end[n_elec][-1]['lev'] = ind
	collect_n_start_end[n_elec][-1]['start'] = min(en_ion)
	collect_n_start_end[n_elec][-1]['end'] = max(en_ion)

#Write the data to files
for n_elec in collect_n_start_end:
	f_write = open(file_n_start_end+'/'+n_elec, 'w')
	for start_end in collect_n_start_end[n_elec]:
		f_write.write('{2} {0} {1}\n'.format(start_end['start']/13.605693, start_end['end']/13.605693, start_end['lev']))
