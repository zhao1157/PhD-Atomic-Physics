#! This scritp is to create the e file
#set the level file
level_file = 'neg'
#set the base index
ind_base = 464

f_write = open('e_'+level_file, 'w')
count = 0
for line in open(level_file):
	count += 1
	lin_splt = line.split()
	JJ = int(lin_splt[3].split('_')[0])
	
	f_write.write('  0 {0:8d}  0   1\n'.format(ind_base+count))
	f_write.write('  1              0.000000\n')
	f_write.write('{0: 15.6E}  {1:f} {2:f}\n'.format(float(lin_splt[2]), float(int(lin_splt[1])), float(JJ+1)))
