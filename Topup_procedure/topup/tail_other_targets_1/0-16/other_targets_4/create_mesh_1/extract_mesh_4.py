#This script is to extract energy mesh from tailed bprm data for each level.
import sys

#Set the directory of correct_match and tailed bprm
correct_match_dir = '../../../../correct_match_n4'
bprm_tailed_dir = '../../combine_tail_3'
num_head_line = 45
#set the number of levels of each symmetry.
sym_level = {'0_0': 18, '0_1': 17, '2_0': 40, '2_1': 41, '4_0': 45, '4_1': 45, '6_0': 39, '6_1': 40, '8_0': 32,
             '8_1': 33, '10_0': 24, '10_1': 26, '12_0': 16, '12_1': 17, '14_0': 10, '14_1': 10, '16_0': 7, '16_1': 4}


#======= BLACK BOX ========
JJ = sys.argv[1]
Pi = sys.argv[2]
#deal with the mismatch so that 'level_thresh_order_3' has the correct ordered levels.
lines_org = open('level_thresh_order_3').readlines()
num_levels = len(lines_org)

correct_match = {}
for line in open(correct_match_dir+'/'+JJ+'_'+Pi): #if empty, make sure no '\n', i.e. 0 CHARACTER.
	line_split = line.split()
	correct_match[line_split[0]] = line_split[1]

f_corrected = open('level_thresh_order_3_corrected', 'w')

line_count = 0
for i in range(num_levels):
	line_count += 1
	if line_count > sym_level[JJ+'_'+Pi]: continue

	if str(i+1) in correct_match:
		level_lowest_thresh = lines_org[int(correct_match[str(i+1)])-1].split()
		if len(level_lowest_thresh) == 1: level_lowest_thresh.append('skip')
		f_corrected.write(level_lowest_thresh[0]+'  '+level_lowest_thresh[1]+'\n')
	else:
		level_lowest_thresh = lines_org[i].split()
		if len(level_lowest_thresh) == 1: level_lowest_thresh.append('skip')
		f_corrected.write(level_lowest_thresh[0]+'  '+level_lowest_thresh[1]+'\n')
f_corrected.close()	
del(lines_org) #release memory, cause it might be very large.

#Now ready to extract the mesh from tailed bprm data.
f_bprm_tail = open(bprm_tailed_dir+'/'+JJ+'_'+Pi+'_bprm_tail', 'r')
f_corrected = open('level_thresh_order_3_corrected', 'r')
f_mesh = open('fine_mesh_bf', 'w')
f_bprm_start = open(JJ+'_'+Pi+'_bprm_start', 'w')

line_count = 0
for level in range(1, 1+num_levels):
	line_count += 1
        if line_count > sym_level[JJ+'_'+Pi]: continue

	#read the lowest threshold energy from corrected fac level.
	line = f_corrected.readline().split()
	fac_level = line[0]
	if line[1] != 'skip':
		lowest_threshold = float(line[1])
		#
		for i in range(1+num_head_line): f_bprm_tail.readline()
		num_point = int(f_bprm_tail.readline().split()[1])
		f_bprm_tail.readline()
		for i in range(1, 1+num_point):
			en_bp = float(f_bprm_tail.readline().split()[0])*13.605693 #in ev
			if en_bp >= lowest_threshold:
				f_mesh.write('{0:s}  {1:12.6E}  '.format(fac_level, en_bp))
				f_bprm_start.write('{0:d}\n'.format(i))
				break
		else:
			print ('Lowest threshold is too large. Something wrong?')	
			raise SystemExit()
	
		for j in range(i+1, 1+num_point):
			f_mesh.write('{0:12.6E}  '.format(float(f_bprm_tail.readline().split()[0])*13.605693))
	else:
		for i in range(1+num_head_line): f_bprm_tail.readline()
		num_point = int(f_bprm_tail.readline().split()[1])
		for i in range(1, 2+num_point): f_bprm_tail.readline()
		f_mesh.write('{0:s}  skip'.format(fac_level))
		f_bprm_start.write('skip\n')
		
	f_mesh.write('\n')





