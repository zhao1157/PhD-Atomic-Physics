#This script is to combine tail and bprm data into one file.
num_head_line = 45
bprm_data_dir = '../../../../../XSECTN_n4' 
sym_level = {'0_0': 18, '0_1': 17, '2_0': 40, '2_1': 41, '4_0': 45, '4_1': 45, '6_0': 39, '6_1': 40, '8_0': 32,
             '8_1': 33, '10_0': 24, '10_1': 26, '12_0': 16, '12_1': 17, '14_0': 10, '14_1': 10, '16_0': 7, '16_1': 4} 
			 
for sym in sym_level:
	JJ_Pi = sym.split('_')		 
	JJ = JJ_Pi[0]
	Pi = JJ_Pi[1]
	
	f_write = open(sym+'_bprm_tail', 'w')
	f_bprm = open(bprm_data_dir+'/'+sym, 'r')
	f_ratio = open(sym+'_ratio', 'w')
	
	for level in range(1, 1+sym_level[sym]):
		num_point_tail = len(open('../generate_PI_2/xsectn_'+sym+'/'+str(level), 'r').readlines())
		f_tail = open('../generate_PI_2/xsectn_'+sym+'/'+str(level), 'r')
		
		#start read bprm data and match at the last point with fac tail
		for i in range(1+num_head_line): f_write.write(f_bprm.readline())
		
		line = f_bprm.readline().split()
		points = num_point_tail-1+int(line[1]) #-1 due to matching point
		f_write.write('  {0:s}{1:10d}\n'.format(line[0], points))
		
		for i in range(int(line[1])): f_write.write(f_bprm.readline())
		
		line = f_bprm.readline()
		f_write.write(line)

		line_bp = line.split()
		line_tail = f_tail.readline().split()
		ratio = float(line_bp[1])/float(line_tail[1])
		f_ratio.write(str(ratio)+'\n')
		
		for line in f_tail:
			line_split = line.split()
			f_write.write('  {0:12.6E} {1:9.3E}\n'.format(float(line_split[0]), float(line_split[1])*ratio))
			
		
