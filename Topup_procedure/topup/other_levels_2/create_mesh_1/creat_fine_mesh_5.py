#! /usr/bin/env python

#This script is to create the fine mesh for all initial levels
import numpy as np

f = open('fine_mesh_bf', 'w')

for line in open('level_thresh_order_mini_diff_4'):
	line_split = line.split()
	
	length = len(line_split)
	
	line_split[-1] = float(line_split[-1])
	line_split[-1] = line_split[-1] if line_split[-1] < 1 else 1
		
	delta = line_split[-1]/10.0
	
	f.write(line_split[0]+' ')
	for num_thresh in range(1, length-2):
		fine_mesh = []
		e1 = float(line_split[num_thresh])+delta
		e2 = float(line_split[num_thresh+1])-delta
		
		if num_thresh < length-3:
			if e2-e1 < 10:
				fine_mesh += list(np.linspace(e1, e2, 10))
			else:
				fine_mesh += list(np.linspace(e1, e2, 20))
		else:
			fine_mesh += list(np.linspace(e1, e2, 300))
	
		for i in range(len(fine_mesh)):
			f.write('{0:15.9E} '.format(fine_mesh[i]))
	f.write('\n')
	
f.close()

#To make sure all the points are different.
#Run an awk program
#import os
#os.popen('./test_same.awk fine_mesh_bf')


