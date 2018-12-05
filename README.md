# PhD-Atomic-Physics
This repository includes the main code I wrote for my research in pursuit of an atomic physics PhD degree at the Ohio State University. Note: usually the order of executing the scripts in a folder is the same as the index just before the extension. For example, *a_1.sh*, and *b_2.sh* are in the same directory, so the order of executing them is *a_1.sh* followed by *b_2.sh*. The same rules applies to directories.

## BPRM/
- Input files for BPRM:
  - *couple_core_e_0.sh*: in stg2, we need to couple the quantumn numbers **S** and **L** of the target states with those of the outer electron, so this script does this job.
  - *recupd_core_2j_p_0.sh*: in recupd, it can be really tedious to manually input the **2J** and **π** values of the target, so this script collects this information and outputs it appropriately.

-------------------  

- Submit PBS jobs: working on the OSU ASC Unity cluster, I used the following two scripts (mainly the first one) to submit thousands of jobs.
  - *f_bf_submit_1.py*: divides a certain energy region into a number of sub-ranges, and the input files are created automatically. The folder **error** contains the index of the sub-range which fails due to some reason, and this script can be modified by just a few lines to resubmit those failed ones.
  - *f_bf_submit_nodes_1.py*: only differs from the one above by one feature, i.e. requesting a certain node for a job. I implemented this feature after the cluster got into some weird problem that caused my jobs to fail on some nodes.

--------------------

- Combine sub-range data into one:
  - *combine_ranges_2.py*: combines the photoionization cross section of many sub-ranges into a whole one. This script was developed in a situation where some of sub-ranges are divided futher into another 10 sub-sub-ranges, so in the script you will see several appearance of `range(10)`.

## Topup_procedure/
In this folder, I show the procedure of doing the level-matching and top up. To match the levels, they are categorized by quantumn numbers **2J** and **π**, and ordered in energy, and the photoionization cross section is plotted for both RDW and BPRM. A level is matched when quantumn numbers **2J** and **π**, energy and photoionization cross section agree well. After being matched, the photoionization cross section of each level is extended to high energy region using RDW method, multiplying a factor to RDW data so that it's continuous from BPRM and RDW. The contribution from other core configurations is added aferwards.  The other bound state levels are collected and the photoionization cross section of them is computed considering all the core configurations. The bound-bound top up calculation is divided into two parts. One is from bound to pure bound states, and the other is to quasi-bound states.

### Topup_procedure/match/
- **bound_levels_0/**: extracts the bound levels that contribute to the photoionization cross section, in terms of **2J** and **π**. 
--------
- **create_mesh_1/**: creates energy mesh for each bound state level. To delineate the edges, 10 points are uniformly assigned between adjacent thresholds. 
- **generate_PI_2/**: after mesh being generated, the scripts in this folder calculates the photoionization cross section.
- **level_identification_3/**: 
  - *plot_n4_background_1.py*: plot the photoionization cross section of RDW and BPRM and see how well they match with each other. Correction is needed if they don't agree well by switching to other reasonable levels.
- **ratio_analysis_4/**: extracts the information of the levels whose ratios fall within a range. 
- **bb_5/**: does the bound-bound top up calculation.
  - *create_e_file.py*: creates e-file needed in opacity calculation. Bound-pure-bound: uncomment lines 72, 78, 79, comment out 73; bound-quasi-bound: comment out lines 72, 78, 79, uncomment 73.
  - *create_f_file.py*: creates f-file needed in opacity calculation. Bound-pure-bound: uncomment line 73, comment out 74; bound-quasi-bound: comment out line 73, uncomment 74.
  
  
  
  
