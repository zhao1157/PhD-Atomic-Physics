#This script is usd to combine small section of photoionization cross section data into one
import os

#================ INPUT ===================
num_head_line = 58 #42: energy lines + the level line
num_level = 8	#number of levels for this initial symmetry
num_subrange = 600	#if ending at 39, then it should be 40 (FILE INDEX RANGES FROM 0 TO 39)
out_file = "XSECTN_total"	#the filename of the output data

#=========================================================================================
#======================== BLOCK BOX, BUT SHOULD BE MODIFIED IN SOME CASE =================
#================================= FILE_NAME[] & RANGE(42) ===============================
#open the individual file
files = []
file_name = []
for index in range(num_subrange):
	if (os.popen('if [ -f XSECTN_'+str(index)+' ]; then echo Yes; else echo No; fi').read().split()[0] == 'Yes'):
		file_name.append("XSECTN_"+str(index))
		files.append(open(file_name[index], 'r'))
	else:
		file_name.append([])
		files.append([])
		
		for i in range(10):
			if (os.popen('if [ -f XSECTN_'+str(index)+'_'+str(i)+' ]; then echo Yes; else echo No; fi').read().split()[0] == 'Yes'):
				file_name[index].append('XSECTN_'+str(index)+'_'+str(i))
				files[index].append(open(file_name[index][i], 'r'))
			else:
				file_name[index].append('skip')
				files[index].append('skip_file')
		skip = 0
		for i in range(10):
			if (file_name[index][i] == 'skip'):
				skip = skip + 1
		if (skip == 10):
			file_name[index] = 'skip'

f_out = open(out_file, 'w')	

#start the processing for all the levels
for level in range(num_level):
	print "level= ", level+1
	first_file = 0
	head = []
	num_points = 0
	XSECTN = []
	
	#collect the data for each level
	for index in range(num_subrange):
		if (file_name[index] == 'skip'):
			continue
		print " "*4+"subrange= ", index
		first_file += 1
		
		if (file_name[index] == 'XSECTN_'+str(index)):
			if (first_file == 1):
				for line_num in range(num_head_line):
					head.append(files[index].readline())
			else:
				for line_num in range(num_head_line):
                                	files[index].readline()
			energy_num_points = files[index].readline().split()
                	num_points += int(energy_num_points[1])
                	zeros = files[index].readline()
                	#now it's time to read the XSECTN data
                	for line_num in range(int(energy_num_points[1])):
        	                XSECTN.append(files[index].readline())			
		else:
			for i in range(10):
				if (file_name[index][i] != 'skip'):
					if (first_file == 1):
                        		      	for line_num in range(num_head_line):
                        		                head.append(files[index][i].readline())
                        		else:
                        		        for line_num in range(num_head_line):
                        		                files[index][i].readline()
					first_file += 1

                        		energy_num_points = files[index][i].readline().split()
                        		num_points += int(energy_num_points[1])
                        		zeros = files[index][i].readline()
                        		#now it's time to read the XSECTN data
                        		for line_num in range(int(energy_num_points[1])):
                	         		XSECTN.append(files[index][i].readline())

	#Now the data for this level has been collected, so it's time to write to the final file.		
	for line_num in range(num_head_line):
		f_out.write(head[line_num])				
	
	f_out.write("  "+energy_num_points[0]+" "*5+str(num_points)+"\n")	
	f_out.write(zeros)
	for xsectn_line in XSECTN:
		f_out.write(xsectn_line)
