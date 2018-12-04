# This script is to combine the tailed bprm and xsectn due to other targets.

#Set directories of xsectn, bprm_start and tailed bprm data.
num_head_line = 45 
xsectn_other_target_dir = '../generate_PI_2'
bprm_start_dir = '../create_mesh_1'
tailed_bprm_dir = '../../combine_tail_3'
#symmetry and its number of levels.
sym_level = {'0_0': 18, '0_1': 17, '2_0': 40, '2_1': 41, '4_0': 45, '4_1': 45, '6_0': 39, '6_1': 40, '8_0': 32,
             '8_1': 33, '10_0': 24, '10_1': 26, '12_0': 16, '12_1': 17, '14_0': 10, '14_1': 10, '16_0': 7, '16_1': 4}

for sym in sym_level:
	[JJ, Pi] = sym.split('_')
	f_write = open(sym+'_bprm_tail_other_targets', 'w')
	f_bprm_tail = open(tailed_bprm_dir+'/'+sym+'_bprm_tail', 'r')
	f_bprm_start = open(bprm_start_dir+'/'+sym+'_bprm_start', 'r')
	
	for level in range(1, 1+sym_level[sym]):
		for i in range(1+num_head_line): f_write.write(f_bprm_tail.readline())
		line_bprm_tail = f_bprm_tail.readline()
		f_write.write(line_bprm_tail)
	
		num_point = int(line_bprm_tail.split()[1])
		f_write.write(f_bprm_tail.readline())
	
		line_bprm_start = f_bprm_start.readline().rstrip()
		if line_bprm_start == 'skip':
			for i in range(num_point): f_write.write(f_bprm_tail.readline())
		else:
			for i in range(int(line_bprm_start)-1): f_write.write(f_bprm_tail.readline())

			f_other_target = open(xsectn_other_target_dir+'/xsectn_'+sym+'/'+str(level))
			for i in range(int(line_bprm_start), 1+num_point): 
				#f_other_target = open(xsectn_other_target_dir+'/xsectn_'+sym+'/'+str(level))
				[en, xsectn]=f_bprm_tail.readline().split()
				
				xsectn = float(xsectn)+float(f_other_target.readline().split()[1])
				f_write.write('  {0:s}  {1:9.3E}\n'.format(en, xsectn))
		
