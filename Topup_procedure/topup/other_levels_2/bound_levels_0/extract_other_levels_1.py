import os
#This is to extract the bound levels that are not included in the BPRM.

#Set the correct_match directory
correct_match_dir = '../../correct_match_n4'
#set the number of levels of each symmetry.
sym_level = {'0_0': 18, '0_1': 17, '2_0': 40, '2_1': 41, '4_0': 45, '4_1': 45, '6_0': 39, '6_1': 40, '8_0': 32,
             '8_1': 33, '10_0': 24, '10_1': 26, '12_0': 16, '12_1': 17, '14_0': 10, '14_1': 10, '16_0': 7, '16_1': 4}

f_write = open('neg', 'w')
for sym_neg in os.popen('ls *_?_neg').read().split():
	sym = sym_neg[:-4]
	if not sym in sym_level:
		for line in open(sym_neg):
			f_write.write(line)
	else:
		correct_match = {}
		for line in open(correct_match_dir+'/'+sym):
			line_split = line.split()
			correct_match[line_split[0]] = line_split[1]
		level = ['hold'] + [i for i in range(1, 1+sym_level[sym])]
		for i in correct_match:
			level[int(i)] = int(correct_match[i])
		
		count = 0
		for line in open(sym+'_neg'):
			count += 1
			if count in level: continue
			f_write.write(line)
		if count < sym_level[sym]:
			print ('error')
			raise SystemExit
