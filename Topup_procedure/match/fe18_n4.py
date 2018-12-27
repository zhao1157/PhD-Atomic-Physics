from pfac import fac
import os

fac.SetAtom('Fe')
fac.Closed('1s')

##Set the target configurations
#fac.Config('T1', '2*7')
#fac.Config('T2', '2*6 3*1')
#fac.Config('T31.4s', '2s2 2p4 4s1')
#fac.Config('T31.4p', '2s2 2p4 4p1')
#fac.Config('T31.4d', '2s2 2p4 4d1')
#
#fac.Config('T32.4s', '2s1 2p5 4s1')
#fac.Config('T32.4p', '2s1 2p5 4p1')
#fac.Config('T32.4d', '2s1 2p5 4d1')
#
##CI
#fac.Config('T31.4f', '2s2 2p4 4f1')
#fac.Config('T32.4f', '2s1 2p5 4f1')
#fac.Config('T33.4*', '2p6 4*1')

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

#Set the quasi-bound configuraitons for TRtable
fac.Config('T23.4*.4*', '2p6 4*2')
fac.Config('T23.4*.5*', '2p6 4*1 5*1')
fac.Config('T23.4*.6*', '2p6 4*1 6*1')
fac.Config('T23.4*.7*', '2p6 4*1 7*1')

fac.Config('T2.4f.4f', '2s2 2p4 4f2')
fac.Config('T2.4f.5*', '2s2 2p4 4f1 5*1')
fac.Config('T2.4f.6*', '2s2 2p4 4f1 6*1')
fac.Config('T2.4f.7*', '2s2 2p4 4f1 7*1')

fac.Config('T3.4f.4f', '2s1 2p5 4f2')
fac.Config('T3.4f.5*', '2s1 2p5 4f1 5*1')
fac.Config('T3.4f.6*', '2s1 2p5 4f1 6*1')
fac.Config('T3.4f.7*', '2s1 2p5 4f1 7*1')

fac.Config('T11.5*.5*', '2*6 5*2')
fac.Config('T11.5*.6*', '2*6 5*1 6*1')
fac.Config('T11.5*.7*', '2*6 5*1 7*1')

fac.Config('T11.6*.6*', '2*6 6*2')
fac.Config('T11.6*.7*', '2*6 6*1 7*1') 

fac.Config('T11.7*.7*', '2*6 7*2')  

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

outfile_tr_b = 'outfile/fe18b.tr'
outfile_tr_a = outfile_rr_b[:-4]+'a.tr'

#Structure
#Bound configurations
fac.Structure(outfile_lev_b, ['T1.2*']) #, 'T1.3*', 'T1.4*', 'T1.5*', 'T1.6*', 'T1.7*', 'T1.8*', 'T1.9*', 'T1.10*'])
fac.Structure(outfile_lev_b, ['T1.3*'])
fac.Structure(outfile_lev_b, ['T1.4*'])
fac.Structure(outfile_lev_b, ['T1.5*'])
fac.Structure(outfile_lev_b, ['T1.6*'])
fac.Structure(outfile_lev_b, ['T1.7*'])
fac.Structure(outfile_lev_b, ['T1.8*'])
fac.Structure(outfile_lev_b, ['T1.9*'])
fac.Structure(outfile_lev_b, ['T1.10*'])

#Target configurations
#fac.Structure(outfile_lev_b, ['T1'])
#fac.Structure(outfile_lev_b, ['T2'])
#fac.Structure(outfile_lev_b, ['T1', 'T2', 'T31.4s', 'T31.4p', 'T31.4d', 'T31.4f', 'T32.4s', 'T32.4p', 'T32.4d', 'T32.4f', 'T33.4*'])

#Quasi-bound configurations
fac.Structure(outfile_lev_b, ['T23.4*.4*', 'T2.4f.4f', 'T3.4f.4f'])
fac.Structure(outfile_lev_b, ['T23.4*.5*', 'T2.4f.5*', 'T3.4f.5*'])
fac.Structure(outfile_lev_b, ['T23.4*.6*', 'T2.4f.6*', 'T3.4f.6*'])
fac.Structure(outfile_lev_b, ['T23.4*.7*', 'T2.4f.7*', 'T3.4f.7*'])

fac.Structure(outfile_lev_b,['T11.5*.5*'])
fac.Structure(outfile_lev_b,['T11.5*.6*'])
fac.Structure(outfile_lev_b,['T11.5*.7*'])

fac.Structure(outfile_lev_b,['T11.6*.6*'])
fac.Structure(outfile_lev_b,['T11.6*.7*'])

fac.Structure(outfile_lev_b,['T11.7*.7*']) 

#Print the energy table
fac.MemENTable(outfile_lev_b)
fac.PrintTable(outfile_lev_b, outfile_lev_a, 1)

##Generate the PI table
##================ For matching ==============
#bound_config = ['T1.2*', 'T1.3*', 'T1.4*', 'T1.5*', 'T1.6*', 'T1.7*', 'T1.8*',
#	        'T1.9*', 'T1.10*']
#free_config = ['T1', 'T2', 'T31.4s', 'T31.4p', 'T31.4d', 'T32.4s', 'T32.4p', 'T32.4d']
#fac.RRTable(outfile_rr_b, bound_config, free_config)
#
##print the rr table
#fac.PrintTable(outfile_rr_b, outfile_rr_a, 1)

#============TR==================================================================
fac.TRTable(outfile_tr_b, ['T1.4*'], ['T23.4*.4*', 'T23.4*.5*', 'T23.4*.6*', 'T23.4*.7*', 
				      'T2.4f.4f', 'T2.4f.5*', 'T2.4f.6*', 'T2.4f.7*', 
				      'T3.4f.4f', 'T3.4f.5*', 'T3.4f.6*', 'T3.4f.7*'], -1)
fac.TRTable(outfile_tr_b, ['T1.5*'], ['T23.4*.5*', 'T2.4f.5*', 'T3.4f.5*', 'T11.5*.5*', 'T11.5*.6*', 'T11.5*.7*'], -1)
fac.TRTable(outfile_tr_b, ['T1.6*'], ['T23.4*.6*', 'T2.4f.6*', 'T3.4f.6*', 'T11.5*.6*', 'T11.6*.6*', 'T11.6*.7*'], -1)
fac.TRTable(outfile_tr_b, ['T1.7*'], ['T23.4*.7*', 'T2.4f.7*', 'T3.4f.7*', 'T11.5*.7*', 'T11.6*.7*', 'T11.7*.7*'], -1)


fac.TRTable(outfile_tr_b,['T1.2*'], ['T1.2*', 'T1.3*', 'T1.4*', 'T1.5*', 'T1.6*', 'T1.7*', 'T1.8*','T1.9*', 'T1.10*'], -1)
fac.TRTable(outfile_tr_b,['T1.3*'], ['T1.3*', 'T1.4*', 'T1.5*', 'T1.6*', 'T1.7*', 'T1.8*','T1.9*', 'T1.10*'], -1)
fac.TRTable(outfile_tr_b,['T1.4*'], ['T1.4*', 'T1.5*', 'T1.6*', 'T1.7*', 'T1.8*','T1.9*', 'T1.10*'], -1)
fac.TRTable(outfile_tr_b,['T1.5*'], ['T1.5*', 'T1.6*', 'T1.7*', 'T1.8*','T1.9*', 'T1.10*'], -1)
fac.TRTable(outfile_tr_b,['T1.6*'], ['T1.6*', 'T1.7*', 'T1.8*','T1.9*', 'T1.10*'], -1)
fac.TRTable(outfile_tr_b,['T1.7*'], ['T1.7*', 'T1.8*','T1.9*', 'T1.10*'], -1)
fac.TRTable(outfile_tr_b,['T1.8*'], ['T1.8*','T1.9*', 'T1.10*'], -1)
fac.TRTable(outfile_tr_b,['T1.9*'], ['T1.9*', 'T1.10*'], -1)
fac.TRTable(outfile_tr_b,['T1.10*'], ['T1.10*'], -1)
#Print trtable
fac.PrintTable(outfile_tr_b, outfile_tr_a, 1)
