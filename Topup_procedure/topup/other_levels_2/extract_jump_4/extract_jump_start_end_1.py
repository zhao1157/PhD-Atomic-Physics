# This script is to extract the ionization thresholds of the transitions at the start and end 
import os

#set the starting energy of photon to search from
en_start = 13.605693 * 90
#set the exponet of the photoionization cross section
exp_pi = ['+02', '+01', '+00']
#Set the path to the file containing the bound levels
file_bound = '../bound_levels_0/neg'
#Set the rrtabble
rrtabel = '../outfile_jump_start_end/fe18a.rr'
#Set the directory where to store the output files
out_file = 'outfile'
##=========== BLACK BOX ==========
#Read the bound levels
bound_levels = []
for line in open(file_bound):
	bound_levels.append(line.split()[0])

#Read the rrtable and extract all the information needed for all bound levels.
os.popen('if [ -d '+out_file+' ]; then rm -rf '+out_file+';fi; mkdir '+out_file+';')
f_rr = open(rrtabel)
for i in range(6):
	f_rr.readline()
nblock = int(f_rr.readline().split()[2])
f_write = {}
for block in range(nblock):
        for i in range(2): f_rr.readline()
        ntrans = int(f_rr.readline().split()[2])
        for i in range(21): f_rr.readline()

        for tran in range(ntrans):
                head = f_rr.readline()
                level = head.split()[0]
                en = float(head.split()[4])
                if not level in bound_levels:
                        for i in range(7): f_rr.readline()
                elif en < en_start:
                        for i in range(7): f_rr.readline()
                else:
                        f_rr.readline()
                        line = f_rr.readline()
                        exp = line.split()[2].strip()[-3:]
			if exp in exp_pi:
				#determine whether the output file is open or not
				if not level in f_write:
					f_write[level] = {}
				if not exp in f_write[level]:
					f_write[level][exp] = open(out_file+'/'+level+'_'+exp, 'w')
			
				f_write[level][exp].write(head)
				f_write[level][exp].write(line)
				for i in range(5): f_write[level][exp].write(f_rr.readline())
                        else:
                                for i in range(5): f_rr.readline()

