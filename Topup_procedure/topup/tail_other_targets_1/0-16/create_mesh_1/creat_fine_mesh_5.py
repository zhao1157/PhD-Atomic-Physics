#This script is to create the mesh for tail with other threshold included.
import numpy as np
import sys

#set the number of levels of each symmetry.
sym_level = {'0_0': 18, '0_1': 17, '2_0': 40, '2_1': 41, '4_0': 45, '4_1': 45, '6_0': 39, '6_1': 40, '8_0': 32,
             '8_1': 33, '10_0': 24, '10_1': 26, '12_0': 16, '12_1': 17, '14_0': 10, '14_1': 10, '16_0': 7, '16_1': 4}

#Specify the correct_match directory from matching background.
correct_match_dir = '../../../correct_match_n4'
#Specify the directory containing the lowest threshold and last energy point information of bprm
en_bp_dir = '../../../extract_bprm_tail_n4_0'

JJ = sys.argv[1]
Pi = sys.argv[2]

#============ BLACK BOX ==============
#deal with the mismatch so that 'level_thresh_order_mini_diff_4' has the correct ordered levels.
lines_org = open('level_thresh_order_mini_diff_4').readlines()

correct_match = {}
for line in open(correct_match_dir+'/'+JJ+'_'+Pi): #if empty, make sure no '\n', i.e. 0 CHARACTER.
	line_split = line.split()
	correct_match[line_split[0]] = line_split[1]

f_corrected = open('level_thresh_order_mini_diff_4_corrected', 'w')

for i in range(len(lines_org)):
	if str(i+1) in correct_match:
		f_corrected.write(lines_org[int(correct_match[str(i+1)])-1])
	else:
		f_corrected.write(lines_org[i])
f_corrected.close()	
del(lines_org) #release memory, cause it might be very large.

#
f_mesh = open('fine_mesh_bf', 'w')
f_en_bp = open(en_bp_dir+'/'+JJ+'_'+Pi+'_endline')

line_count = 0

for line in open('level_thresh_order_mini_diff_4_corrected'):
	line_count += 1
	if line_count > sym_level[JJ+'_'+Pi]: continue

	line_split = line.split()
	index_level = line_split[0] #in case it's overwritten by the one following line of code.
	
	length = len(line_split)
	if length < 2: 
		print ('length < 2')
		raise SystemExit
		
	line_split[-1] = float(line_split[-1])
	line_split[-1] = line_split[-1] if line_split[-1] < 1 else 1
		
	delta = line_split[-1]/10.0
	
	fine_mesh = []
	
	line_bp = f_en_bp.readline().split()
	lowest_threshold = abs(float(line_bp[0]))*13.605693 #in ev
	end_energy = float(line_bp[1])*13.605693 #in ev
	#===============end of bprm data =========
	
	start = 0 
	for num_thresh in range(1, length-1):
		#find the first threshold that's larger than end_energy.
		if float(line_split[num_thresh]) > end_energy:
			start = num_thresh
			line_split[num_thresh-1] = end_energy #for later use
			break
	
	if start == 0:
		fine_mesh += list(np.linspace(end_energy, lowest_threshold+500*13.605693, 400))
	else:
		for num_thresh in range(start-1, length-2): 
			e1 = float(line_split[num_thresh])+delta if num_thresh != start-1 else float(line_split[num_thresh])
			e2 = float(line_split[num_thresh+1])-delta
			fine_mesh += list(np.linspace(e1, e2, 10))
		fine_mesh += list(np.linspace(float(line_split[-2])+delta, lowest_threshold+500*13.605693, 300))

	f_mesh.write(index_level+' ')
	
	for i in range(len(fine_mesh)):
		f_mesh.write('{0:15.9E} '.format(fine_mesh[i]))
	f_mesh.write('\n')
	
f_mesh.close()

##To make sure all the points are different.
##Run an awk program
#import os
#os.popen('./test_same.awk fine_mesh_bf')
#
#
