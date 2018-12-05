#This script is to find the level information for different raios.

#note the levels and ratios are written in the same order
level_file = '../level_identification_3/total_line'
ratio_file = '../../topup/tail_other_targets_1/0-16/combine_tail_3/ratio'

#set the ratio we want to catogarize.  Note the (ratio > the largest) will be collected.
ratios = range(5) # from 0 to n, in ascending order and delta n = 1 

f_level = open(level_file)
ratios_copy = ratios + [ratios[-1]+1]
file_ratio_levels = [open('ratio_'+str(i)+'_levels', 'w') for i in ratios_copy]

for ratio_line in open(ratio_file):
	ratio = float(ratio_line.strip())
	
	if int(ratio+0.5) in ratios:
		ratio_int = int(ratio+0.5)
	else:
		ratio_int = ratios[-1]
	
	file_ratio_levels[ratio_int].write(f_level.readline())
	
	


