#set the starting and ending energy of photon
en_start = 13.605693 * 100
en_end = 13.605693 * 1000
#set the exponet of the photoionization cross section
exp_pi = ['+01', '+00', '-01']
#set the bound level index
ind_bound = '685'
#Specify the energy and rr file.
f_rr_name = '../outfile/fe18a.rr'

#===================BLACK BOX===================
f_rr = open(f_rr_name, 'r')

####reading rr file
for i in range(6): 
	f_rr.readline()

nblock = int(f_rr.readline().split()[2])

#open files for writing
files = {} 
for i in exp_pi:
	files[i] = open('pi_' + i, 'w')

JJ_Pi = {}
for block in range(nblock):
	for i in range(2): f_rr.readline()
	ntrans = int(f_rr.readline().split()[2])
	for i in range(21): f_rr.readline()
	
	for tran in range(ntrans):
		head = f_rr.readline()
		level = head.split()[0]	
		en = float(head.split()[4])
		if level != ind_bound:
			for i in range(7): f_rr.readline()
		elif en < en_start or en > en_end:
			for i in range(7): f_rr.readline()
		else:
			f_rr.readline()
			line = f_rr.readline()
			exp = line.split()[2].strip()[-3:]
			if exp in exp_pi:
				files[exp].write(head)
				files[exp].write(line)
				for i in range(5): files[exp].write(f_rr.readline())
			else:
				for i in range(5): f_rr.readline()
		

