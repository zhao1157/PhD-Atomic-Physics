#! /usr/local/anaconda3/bin/python

#This script is to extract energy and to create the e-file

#set parameters
#The first file is the energy file, the rest files are all the relevant transition files. 
file_en_454_rest = ['../outfile/fe18a.en', '../outfile/fe18a.tr']	#['fe17a_L.en', 'fe17a_L_454.tr', 'fe17a_L_rest.tr']
#set the lowest target energy
en_lowest_target = 1.26007280E+03	 #1.26005903E+03 #1.26009943E+03
#Set the charge of the target
charge_target = 17
#Set the file of the bound levels included in rm.
file_bound_rm = '../level_identification_3/total_levels_corrected'
#set the lowest 2J value
JJ_Min = 0

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

#read the bound rm levels
bound_rm = [line.rstrip() for line in open(file_bound_rm)]
upper = set() 	#contain the upper level indices
lower = set()	#contain the lower level indices
############### II #############
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
			#to make sure the transitions are from bound to quasi-bound
			##if en_dict[line[2]]['energy'] < 0 and en_dict[line[0]]['energy'] < 0 and not (line[0] in bound_rm and line[2] in bound_rm): 
			if en_dict[line[2]]['energy'] < 0 and en_dict[line[0]]['energy'] > 0: 
				if not line[0] in bound_rm:	
					upper.add(line[0])
				###UNcomment out the following 2 lines for pure-bound transitions.
				##if not line[2] in bound_rm:
				##	lower.add(line[2])
				
	f_read.close()	
#print ('extra_lower: {0}'.format(len(lower)))

#Here it works in upper and lower levels never overlap.
upper = list(upper)			
lower = list(lower)
#print (len(lower), len(upper))

############### III #############
#concatenate all levels into one
all_levels = []
all_levels.extend(lower)
all_levels.extend(upper)
all_levels = list(set(all_levels))

print ('extra_lower: {0}'.format(len(all_levels)))
#print (len(all_levels))

############### IV ##############
#Now we are ready to group the energy levels by 2J_Pi
e_file = {}
for lev in all_levels:
	key = en_dict[lev]['2J']+'_'+ en_dict[lev]['Pi']
	if not key in e_file:
		e_file[key]=[lev]
	else:
		e_file[key].append(lev)
	
#Now we are ready to print out the levels according to 2J_Pi.
JJ_Max = JJ_Min 
for JJ_Pi in e_file:
	JJ=int(JJ_Pi.split('_')[0])
	if JJ_Max < JJ:
		JJ_Max = JJ
#print ('JJ_MAX={0}'.format(JJ_Max))

su=0

for JJ in range(JJ_Min, JJ_Max+2, 2): 
	for Pi in range(2):
		JJ_Pi = str(JJ)+'_'+str(Pi)
		if JJ_Pi in e_file:
			num_lev = len(e_file[JJ_Pi])
			su = su+num_lev
			print('{0:>3s}{1:>4s}{2:>4s}{3:>7s}'.format('0', str(JJ), str(Pi), '1'))
			print('{0:>5s}{1:>22.6f}'.format(str(num_lev), 0))
			for lev in e_file[JJ_Pi]:
				en_lev = en_dict[lev]['energy']
				vn_lev = en_dict[lev]['vn']
				print('{0:>14.6E}{1:>11.5f}'.format(en_lev, vn_lev))
		
#print (su)



		
