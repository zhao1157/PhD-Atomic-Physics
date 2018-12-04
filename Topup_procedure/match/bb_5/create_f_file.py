#! /usr/local/anaconda3/bin/python

#This script is to extract energy and to create the e-file
#to run this script with python3, ./create_e_file.py

#set parameters
#The first file is the energy file, the second is the one contains part of the 454 levles,
#the third is the one contains the none of the 454 levels.
file_en_454_rest = ['../outfile/fe18a.en', '../outfile/fe18a.tr']	#['fe17a_L.en', 'fe17a_L_454.tr', 'fe17a_L_rest.tr']
#Set the file of the bound levels included in rm.
file_bound_rm = '../level_identification_3/total_levels_corrected'
#set the lowest target energy
en_lowest_target = 1.26007280E+03	 #1.26005903E+03 #1.26009943E+03
#Set the charge of the target
charge_target = 17

#==========================BLACK BOX=================================
#       ===============================================
#            ===================================
read_en_454_rest = []

for f in file_en_454_rest:
	read_en_454_rest.append(open(f, 'r'))

############## I #############
#create the energy table using dict.
for i in range(6):
	read_en_454_rest[0].readline()
nblocks = read_en_454_rest[0].readline().split()[2]
read_en_454_rest[0].readline() #now you are at the end of the headlines.

#define en_dict as a dictionary which will contains the level information.
en_dict = {}
keys = ['energy', 'Pi', 'vn', '2J']

for block in range(int(nblocks)):
	read_en_454_rest[0].readline()
	read_en_454_rest[0].readline()
	
	nlev = read_en_454_rest[0].readline().split()[2]
	read_en_454_rest[0].readline()
	for lev in range(int(nlev)):
		line = read_en_454_rest[0].readline().split()
		values = [(float(line[2])-en_lowest_target)/13.605693/charge_target/charge_target, line[3], int(line[4])//100, line[5]]
		en_dict[line[0]] = dict(zip(keys, values))

read_en_454_rest[0].close()

tr_table = {}	#declare the dictionary that will contains the transition table.

############### II #############
#read the bound rm levels
bound_rm = [line.rstrip() for line in open(file_bound_rm)]
#read the transition files to pick out the desired transition information.
for f_read in read_en_454_rest[1:]:
	for skip in range(6):
		f_read.readline()
	nblocks = f_read.readline().split()[2]
	
	#read the block data
	for block in range(int(nblocks)):
		f_read.readline()
		f_read.readline()
		ntrans = f_read.readline().split()[2]
		f_read.readline()
		f_read.readline()
		f_read.readline()
		#read the transition data
		for trans in range(int(ntrans)):
			line = f_read.readline().split()
			#to make sure the transitions are from bound to bound 
			upper = en_dict[line[0]]
			lower = en_dict[line[2]]
			#if lower['energy'] < 0 and upper['energy'] < 0 and not (line[0] in bound_rm and line[2] in bound_rm):
			if lower['energy'] < 0 and upper['energy'] > 0: 
				if not line[0] in tr_table:
					tr_table[line[0]] = {}
				if not lower['2J']+'_'+lower['Pi'] in tr_table[line[0]]:
					tr_table[line[0]][lower['2J']+'_'+lower['Pi']] = {}
				if not line[2] in tr_table[line[0]][lower['2J']+'_'+lower['Pi']]:
					tr_table[line[0]][lower['2J']+'_'+lower['Pi']][line[2]] = {'gf':float(line[5]), \
																	'A':float(line[6])}
					
############### III ##############
#Now let's print out the tables.
for upper in tr_table:
	JJ_upper = en_dict[upper]['2J']
	Pi_upper = en_dict[upper]['Pi']
	for JJ_Pi_lower in tr_table[upper]:
		JJ_lower = JJ_Pi_lower.split('_')[0]
		Pi_lower = JJ_Pi_lower.split('_')[1]
		length = len(tr_table[upper][JJ_Pi_lower])
		print ('{0:>5s}{1:>5s}{2:>5s}{3:>10s}{4:>5s}{5:>5s}'.format('0', \
					JJ_upper, Pi_upper, '0', JJ_lower, Pi_lower))
		print ('{0:>5s}{1:>5d}{2:>7s}{3:>13s}{4:>10s}{5:>3s}{6:>4s}{7:>3s}{8:>5s}{9:>11s}'.format(\
					'1', length, 'RE1', 'RE2', 'GFL', '-', 'E1', '-', 'GFV', 'A(E1)*S'))
		
		i = 0
		for lower in tr_table[upper][JJ_Pi_lower]:
			i = i+1
			gf_A = tr_table[upper][JJ_Pi_lower][lower]
			print ('{0:1s}{1:5d}{2:>14.6E}{3:>14.6E}{4:11.3E}{5:11.3E}{6:11.3E}'.format(\
					'1', i, en_dict[upper]['energy'], en_dict[lower]['energy'],gf_A['gf'],\
					 gf_A['gf'], gf_A['A']))	
			
