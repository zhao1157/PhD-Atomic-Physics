from pfac import fac
import os

fac.SetAtom('Fe')
fac.Closed('1s')

#Set the target configurations
fac.Config('T1', '2*7')
fac.Config('T2', '2*6 3*1')
fac.Config('T31.4s', '2s2 2p4 4s1')
fac.Config('T31.4p', '2s2 2p4 4p1')
fac.Config('T31.4d', '2s2 2p4 4d1')

fac.Config('T32.4s', '2s1 2p5 4s1')
fac.Config('T32.4p', '2s1 2p5 4p1')
fac.Config('T32.4d', '2s1 2p5 4d1')

#other target configurations
fac.Config('T31.4f', '2s2 2p4 4f1')
fac.Config('T32.4f', '2s1 2p5 4f1')
fac.Config('T33.4*', '2p6 4*1')
fac.Config('T4', '2*6 5*1')
fac.Config('T5', '2*6 6*1')
fac.Config('T6', '2*6 7*1')
fac.Config('T7', '2*6 8*1')
fac.Config('T8', '2*6 9*1')
fac.Config('T9', '2*6 10*1')

#Set the bound configurations
fac.Config('T1.2*', '2*8')
fac.Config('T1.3*', '2*7 3*1')
fac.Config('T1.4*', '2*7 4*1')
fac.Config('T1.5*', '2*7 5*1')
fac.Config('T1.6*', '2*7 6*1')
fac.Config('T1.7*', '2*7 7*1')
fac.Config('T1.8*', '2*7 8*1')
fac.Config('T1.9*', '2*7 9*1')
fac.Config('T1.10*', '2*7 10*1')

#Now compute the structures
fac.ConfigEnergy(0)
fac.OptimizeRadial(['T1.2*'])
fac.ConfigEnergy(1)

#Create the directory to contain output files.
os.system('if [ -d outfile ]; then rm -rf outfile; fi; mkdir outfile')

outfile_lev_b = 'outfile/fe18b.en'
outfile_lev_a = outfile_lev_b[:-4]+'a.en'

outfile_rr_b = 'outfile/fe18b.rr'
outfile_rr_a = outfile_rr_b[:-4]+'a.rr'

#Structure
#Bound configurations
fac.Structure(outfile_lev_b, ['T1.2*'])
fac.Structure(outfile_lev_b, ['T1.3*'])
fac.Structure(outfile_lev_b, ['T1.4*'])
fac.Structure(outfile_lev_b, ['T1.5*'])
fac.Structure(outfile_lev_b, ['T1.6*'])
fac.Structure(outfile_lev_b, ['T1.7*'])
fac.Structure(outfile_lev_b, ['T1.8*'])
fac.Structure(outfile_lev_b, ['T1.9*'])
fac.Structure(outfile_lev_b, ['T1.10*'])

#Target configurations
#mixing 
fac.Structure(outfile_lev_b, ['T1', 'T2', 'T31.4s', 'T31.4p', 'T31.4d', 'T31.4f', 'T32.4s', 'T32.4p', 'T32.4d', 'T32.4f', 'T33.4*', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9'])
#Print the energy table
fac.MemENTable(outfile_lev_b)
fac.PrintTable(outfile_lev_b, outfile_lev_a, 1)

#Generate the PI table
##================ For matching ==============
bound_config = ['T1.2*', 'T1.3*', 'T1.4*', 'T1.5*', 'T1.6*', 'T1.7*', 'T1.8*',
	        'T1.9*', 'T1.10*']
#free_config = ['T1', 'T2', 'T31.4s', 'T31.4p', 'T31.4d', 'T32.4s', 'T32.4p', 'T32.4d']
#fac.RRTable(outfile_rr_b, bound_config, free_config)

##print the rr table
#fac.PrintTable(outfile_rr_b, outfile_rr_a, 1)

#============== For topup other target configurations ==========
free_config = ['T31.4f', 'T32.4f', 'T33.4*', 'T4', 'T5', 'T6', 'T7', 'T8', 'T9']
fac.RRTable(outfile_rr_b, bound_config, free_config)

#print the rr table
fac.PrintTable(outfile_rr_b, outfile_rr_a, 1)
