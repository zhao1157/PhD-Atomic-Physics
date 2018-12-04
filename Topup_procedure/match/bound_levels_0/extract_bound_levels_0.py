#This is to extract the bound levels that contribute to the PI cross section, in terms of
#2J_Pi

#Specify the energy and rr file.
f_en_name = '../outfile/fe18a.en'
f_rr_name = '../outfile/fe18a.rr'

#Specify the number of electrons of bound configurations
n_ele_bound = 10 
charge_target = 17
#Specify the ground state energy of the target, which will be duducted from all levels
#****USE THE ENERGY BEFORE MIXING DIFFERENT TARGET CONFIGURATIONS.
en_grd_target = 1.26007280E+03 #1.25614084E+03 #1.26032748E+03 #1.25639550E+03 #1.26005903E+03 #1.26007280E+03 #1.35525680E+03

#===================BLACK BOX===================
f_en = open(f_en_name, 'r')
f_rr = open(f_rr_name, 'r')

####reading energy file
for i in range(6): 
	#next(f_en) #this line should work, however python2 complains "Mixing iteration and
	#read methods would lose data"
	f_en.readline()

nblock = int(f_en.readline().split()[2])
#print (nblock)
f_en.readline()

keys = ['energy', 'Pi', 'vnl', 'JJ']
lev = {}
for block in range(nblock):
	f_en.readline()
	if int(f_en.readline().split()[2]) == n_ele_bound:
		nlev = int(f_en.readline().split()[2])
		f_en.readline()
		for i in range(nlev):
			line = f_en.readline().split()
			line[2] = float(line[2])
			lev[line[0]] = {}
			lev[line[0]] = dict(zip(keys, line[2:6]))		
	else:
		nlev = int(f_en.readline().split()[2])
		f_en.readline()
		for i in range(nlev): f_en.readline()
			
####reading rr file
for i in range(6): 
	#next(f_en) #this line should work, however python2 complains "Mixing iteration and
	#read methods would lose data"
	f_rr.readline()

nblock = int(f_rr.readline().split()[2])

JJ_Pi = {}
for block in range(nblock):
	for i in range(2): f_rr.readline()
	ntrans = int(f_rr.readline().split()[2])
	for i in range(21): f_rr.readline()
	
	for tran in range(ntrans):
		level = f_rr.readline().split()[0]	
		if lev[level]['JJ']+'_'+lev[level]['Pi'] in JJ_Pi:
			if not level in JJ_Pi[lev[level]['JJ']+'_'+lev[level]['Pi']]:
				JJ_Pi[lev[level]['JJ']+'_'+lev[level]['Pi']].append(level)
		else:
			JJ_Pi[lev[level]['JJ']+'_'+lev[level]['Pi']] = []
			JJ_Pi[lev[level]['JJ']+'_'+lev[level]['Pi']].append(level)
		for i in range(7): f_rr.readline()

#Now all the transitions are organized in JJ_Pi, we need to put the levels in each symmetry
#in ascending order.

for symtry in JJ_Pi:
	#put the levels in ascending order
	for i in range(len(JJ_Pi[symtry])-1):
		for j in range(i+1, len(JJ_Pi[symtry])):
			if lev[JJ_Pi[symtry][i]]['energy'] > lev[JJ_Pi[symtry][j]]['energy']:
				temp = JJ_Pi[symtry][i]
				JJ_Pi[symtry][i] = JJ_Pi[symtry][j]
				JJ_Pi[symtry][j] = temp
	print (symtry, len(JJ_Pi[symtry]))
	
#Now we are ready to output the levels of negative and positive energy in different files.
for symtry in JJ_Pi:
	f_neg = open(symtry+'_neg', 'w')	
	f_opo = open(symtry+'_opo', 'w')
	for level in JJ_Pi[symtry]:
		if lev[level]['energy'] < en_grd_target:
			f = f_neg
		else:
			f = f_opo
		f.write('{0:6s}{1:6s}{2:9.7f}{3:>6s}\n'.format(level, lev[level]['vnl'][:-2], (lev[level]['energy']-en_grd_target)/13.605693/charge_target/charge_target, symtry))
	f_neg.close()
	f_opo.close()
	
	
	
	
	
	







