#This is to extract the threshold and last point in bprm data for tail-processing use.

#Specify the directory of BPRM data
bp_data_dir = '../../../XSECTN_n4/'
#Specify the number of head lines
num_head_line = 45 

sym_level = {'0_0': 18, '0_1': 17, '2_0': 40, '2_1': 41, '4_0': 45, '4_1': 45, '6_0': 39, '6_1': 40, '8_0': 32,
	     '8_1': 33, '10_0': 24, '10_1': 26, '12_0': 16, '12_1': 17, '14_0': 10, '14_1': 10, '16_0': 7, '16_1': 4}

for JJ in range(0, 17, 2):
	for Pi in range(2):
		f_bprm = open(bp_data_dir+'/'+str(JJ)+'_'+str(Pi), 'r')
		f_endline = open(str(JJ)+'_'+str(Pi)+'_endline', 'w')
		
		for level in range(sym_level[str(JJ)+'_'+str(Pi)]):
			for i in range(num_head_line+1): f_bprm.readline()
			line_bp = f_bprm.readline().split()
			lowest_threshold = line_bp[0]
			
			for i in range(int(line_bp[1])): f_bprm.readline()
			end_energy = f_bprm.readline().split()[0]
			
			f_endline.write(lowest_threshold + ' ' + end_energy + '\n')
			
