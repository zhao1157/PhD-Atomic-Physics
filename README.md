# PhD-Atomic-Physics
This repository includes the main code I wrote for my research in pursuit of an atomic physics PhD degree at the Ohio State University. I mainly programmed in **Python**, in which sometimes **Bash** commands are executed, and in some cases, I even used **AWK** as I was learning it and felt it was really cool to process files. I used **Gnuplot** a lot especially in the level-matching step where I have to plot hundreds of figures. Sometimes I used **Python** to plot, e.g. the figures I made for my paper (see **paper/**).  Note: usually the order of executing the scripts in a folder is the same as the index just before the extension. For example, *a_1.sh*, and *b_2.sh* are in the same directory, so the order of executing them is *a_1.sh* followed by *b_2.sh*. The same rules applies to directories.

If you are interested in doing the top-up calculation for other ions, feel free to download the whole directory of **Topup_procedure/** and you are all set to start your work in that directory.

## I. BPRM/
- Input files for BPRM:
  - *couple_core_e_0.sh*: in stg2, we need to couple the quantumn numbers **S** and **L** of the target states with those of the outer electron, so this script does this job.
  - *recupd_core_2j_p_0.sh*: in recupd, it can be really tedious to manually input the **2J** and **π** values of the target, so this script collects this information and outputs it appropriately.

-------------------  

- Submit PBS jobs: working on the OSU ASC Unity cluster, I used the following two scripts (mainly the first one) to submit thousands of jobs.
  - *f_bf_submit_1.py*: divide a certain energy region into a number of sub-ranges, and the input files are created automatically. The folder **error** contains the index of the sub-range which fails due to some reason, and this script can be modified by just a few lines to resubmit those failed ones.
  - *f_bf_submit_nodes_1.py*: only differ from the one above by one feature, i.e. requesting a certain node for a job. I implemented this feature after the cluster got into some weird problem that caused my jobs to fail on some nodes.

--------------------

- Combine sub-range data into one:
  - *combine_ranges_2.py*: combine the photoionization cross section of many sub-ranges into a whole one. This script was developed in a situation where some of sub-ranges are divided futher into another 10 sub-sub-ranges, so in the script you will see several appearance of `range(10)`.

## II. Topup_procedure/
In this folder, I show the procedure of doing the level-matching and top up. To match the levels, they are categorized by quantumn numbers **2J** and **π**, and ordered in energy, and the photoionization cross section is plotted for both RDW and BPRM. A level is matched when quantumn numbers **2J** and **π**, energy and photoionization cross section agree well. After being matched, the photoionization cross section of each level is extended to high energy region using RDW method, multiplying a factor to RDW data so that it's continuous from BPRM and RDW. The contribution from other core configurations is added aferwards.  The other bound state levels are collected and the photoionization cross section of them is computed considering all the core configurations. The bound-bound top up calculation is divided into two parts. One is from bound to pure bound states, and the other is to quasi-bound states.

### 1. match/
- **bound_levels_0/**: extract the bound levels that contribute to the photoionization cross section, in terms of **2J** and **π**. 
  - **extract_bound_levels_0.py**: input the files that contain the energy and rrtable, the number of electrons of the bound
    configurations, the charge of the core confgurations, and the energy of the ground state of the core configurations in unit of ev.
    Note it is more accurate to use the energy of the ground state of the core with same-n-complex configuration interaction, though
    different-n-complex configuration interaction of the core configurations is used to maximally reproduce the background of BPRM 
    calculation. It outputs the levels in energy ascending order for each symmetry **2J_π**, and the negative and positive levels are 
    separated.
--------
- **create_mesh_1/**: create energy mesh for each bound state level. To delineate the edges, 10 points are uniformly assigned between
  adjacent thresholds. 
  - **extract_trans_awk_1.sh**: collect the transition information for the levels of interest, i.e. the header line for each transition.
  Usually we need to create a symlink that points to a file which contains the levels we are interested in, e.g. 
  `ln -s ../bound_levels_0/0_0_neg bound_levels_0` (see script **run_JJ_Pi.sh** in **match/** directory).
  - **collect_thresh_awk_2.sh**: collect the various thresholds for each level, and output the level index and its thresholds in one 
  single line.
  - **order_thresh_awk_3.sh**: sort the thresholds for each level in ascending order, and append each level with an energy that is 
  105 Ry (or another range of your interest) more than the lowest threshold, and remove other thresholds that are the same as 
  one threshold.
  - **add_mini_diff_awk_4.sh**: append the smallest difference between adjacent thresholds at the end of each line for each level. This
  value is useful when creating energy mesh and 10th of it is used as the increment. So in this way we try to delineat the edges of 
  various transitions.
  - **creat_fine_mesh_5.py**: create an energy mesh for each level, with 10 points in any adjacent shresholds, and 20 points between the 
  last threshold and the maximal energy point.
  - **test_same.awk**: it is called inside of **creat_fine_mesh_5.py** to test the fine mesh whether the adjacent points are the same 
  or not. Usually I do not use it.
  - **run.sh**: show the order of executing the scripts above. It is usually called in a loop to run these steps.
--------
- **generate_PI_2/**: after mesh being generated, the scripts in this folder calculate the photoionization cross section.
  - **fe18_n3.py**: load the existing energy binary file and RRTable binary file and interpret and extrapolate the photoionization 
  cross section for each level in the energy mesh created in **create_mesh_1/**. In this script, we use **fac.InterpCross()** to 
  output the
  data for each transition and then to do the summation over all transitions for each level. We can also use **fac.TotalPICross()** to 
  get the summed result, but in many situtations the energy mesh and number of transitions are large which results in the large memory
  requirement. Thus we abandon it in general.
  - **add_awk.sh**: after **fac.InterpCross()** generates the data for all transitions, it reads the data and sums it up in unit of Mb.
--------
- **level_identification_3/**: 
  - *plot_n4_background_1.py*: plot the photoionization cross section of RDW and BPRM and see how well they match with each other. Correction is needed if they don't agree well by switching to other reasonable levels.
--------
- **ratio_analysis_4/**: extract the information of the levels whose ratios fall within a range. This script is useful if you want to
  get a rough idea of how well the calculation of BPRM and RDW agrees with each other at the last point, and what kind of levels do well
  and not well. The order of the levels written in files **level_file** and **ratio_file** has to be the same. Usually it is 0_0 (2J_π), 
  0_1, 2_0, 2_1, ..., 16_0, 16_1 for Fe XVII, but of course it can vary as long as they are in the same fashion in these two files.
--------
- **bb_5/**: does the bound-bound top up calculation.
  - *create_e_file.py*: create e-file needed in opacity calculation. In line 7, variable **ind_max_remove** represents the maximum level
    index that bound-quasi-bound transitions should be neglected as they are already included in BPRM. In the **fac.Structure()** part,
    the bound configurations have to be in front of the other quasi-bound configurations. In line 73, it excludes the transitions that are
    from the positive-energy levels, the transitions that have already been included in BPRM stgbb, and the ones that have already been 
    included in bound-free, i.e. resonances due to n=2 core configurations coupled with an outer electron. In list **file_en_454_rest**, 
    the first file has to be energy file, followed by the transition files. These transition files have to share the same energy file,
    otherwise when reading different transition files, levels will be messed up.
  - *create_f_file.py*: creates f-file needed in opacity calculation. The same variable settings as in file *create_e_file.py*.
  
### 2. topup/
In this folder, I will extend the BPRM data to higher energy region using RDW method, add the contribution from other core configurations, and include the other bound state levels that are not included in BPRM calculation. To calculate the photoionization cross section tail, for each bound state level, I multiply the RDW value at the last energy point in BPRM calculation so that it's equal to the BPRM value, and this factor is applied to all the rest RDW values in the higher energy region. The energy mesh used is divided into two parts. One is the mesh used in BPRM claculation from the lowest ionization threshold to the last point. The other is from the last point in BPRM claculation to 500 Ry of photoelectron energy, and it's created such that 10 points are assigned uniformly between adjacent thresholds of other core configurations that I'm going to describe next. The contribution from other core configurations are added using the mesh that has already considered the thresholds of these core configurations. Lastly, the other bound state levles are included, considering the contribution from all the core configurations used in BPRM and others as described above.

#### 2.1. extract_bprm_tail_n4_0/
This script is used to extract the threshold and last point in bprm data for tail-processing.

#### 2.2. tail_other_targets_1/0-16/ 
- **bound_levels_0/**: only consider the transitions to other core configurations as we want to extract the thresholds due to them, so
  that the energy mesh can be created appropriately.
    - **extract_bound_levels_0.py**: ***update***
--------
- **create_mesh_1/**: the filenames of these scripts are the same as before, but the content can be drastically different. For each level, the tail is created so that any adjacent thresholds have 10 points between them. 
--------
- **generate_PI_2/**: only the transitions due to the core configuraitons included in BPRM calculation are needed. 
--------
- **combine_tail_3/**: attach the scaled RDW tail to BPRM and outputs the ratio used for each level.
--------
- **other_targets_4/**: I'm going to add the contribution from other core configurations to the tailed-BPRM data. Before proceeding, I need to create a symlink to '../bound_levels_0/'.
  - **create_mesh_1/**: extract the energy mesh for each level.
  - **generate_PI_2/**: calculate the photoionization cross section.
  - **combine_other_targets_3/**: combine the tailed-BPRM data with those in **generate_PI_2/**.

#### 2.3. other_levels_2/
I'm going to collect all the other bound levels and calculate the photoionization cross section due to the core configurations included in BPRM calculation and the above top up calculation.
- **bound_levels_0/**: extract the bound levels that contribute to the photoionization cross section, in terms of **2J** and **π**. 
--------
- **create_mesh_1/**: create energy mesh for each bound state level. To delineate the edges, 10 points are uniformly assigned between adjacent thresholds. 
--------
- **generate_PI_2/**: after mesh being generated, calculate the photoionization cross section.

### 3. fe17_fe18_matched_levels/
In this folder, the photoionization cross section of the matched levels are shown. The oscillation at the right end of BPRM is removed and not counted in the opacity calculation.

## III. paper/
In this folder, it contains the scripts that I used to create the plots in the relevant paper (link to be updated).
