# PhD-Atomic-Physics
This repository includes the main code I wrote for my research in pursuit of an atomic physics PhD degree at the Ohio State University. I mainly programmed in *Python*, in which sometimes *Bash* commands are called, and in some cases, I even used *AWK* as I was learning it and felt it was really cool to use it to process files. I used *Gnuplot* a lot especially in the level-matching step where I had to plot hundreds of figures. Sometimes I used *Python* to plot, e.g. the figures I made for my paper (see **paper/**).  Note: usually the order of executing the scripts in a folder is the same as the index just before the extension and just after '_'. For example, *a_1.sh*, and *b_2.sh* are in the same directory, so the order of executing them is *a_1.sh* followed by *b_2.sh*. The same rules applies to directories.

![Image of topup_procedure](https://github.com/zhao1157/PhD-Atomic-Physics/blob/master/Topup_procedure/topup_procedure.png)

If you are interested in doing the top-up calculation for other ions, feel free to download the directories **match/** and **topup/** in **Topup_procedure/** and you are all set to start your work in that directory.

## I. BPRM/
- Input files for BPRM:
  - *core_lsp_0.py*: in stg2, there might be tens of or even a few hundred target terms needed to be collected from superstructure
    output, so it can be tedious to type them in the input file. Thus this simple script just does this job.
  - *couple_core_e_0.sh*: in stg2, we need to couple the quantumn numbers *S* and *L* of the target states with those of the outer electron, so this script does this job.
  - *recupd_core_2j_p_0.sh*: in recupd, it can be really tedious to manually input the *2J* and *π* values of the target, so this script collects this information and outputs it appropriately.

-------------------  

- Submit PBS jobs: working on the OSU ASC Unity cluster, I used the following two scripts (mainly the first one) to submit thousands of jobs.
  - *f_bf_submit_1.py*: divide a certain energy region into a number of sub-ranges, and the input files are created automatically. The folder **error** contains the index of the sub-range which fails due to some reason, and this script can be modified by just a few lines to resubmit those failed ones.
  - *f_bf_submit_nodes_1.py*: only differ from the one above by one feature, i.e. requesting a certain node for a job. I implemented this feature after the cluster got into some weird problem that caused my jobs to fail on some nodes.

--------------------

- Combine sub-range data into one:
  - *combine_ranges_2.py*: combine the photoionization cross section of many sub-ranges into a whole one. This script was developed in a situation where some of sub-ranges are divided futher into another 10 sub-sub-ranges, so in the script you will see several appearances of `range(10)`.

## II. Topup_procedure/
In this folder, I show the procedure of doing the level-matching and top up. To match the levels, they are categorized by quantumn numbers *2J* and *π*, and ordered in energy, and the photoionization cross section is plotted for both RDW and BPRM. A level is matched when quantumn numbers *2J* and *π*, energy and photoionization cross section agree well. After being matched, the photoionization cross section of each level is extended to high energy region using RDW method. The contribution from other core configurations is added aferwards.  The other bound state levels are collected and the photoionization cross section of them is computed considering all the core configurations. The bound-bound top up calculation is divided into two parts. One is from bound to pure bound states, and the other is to quasi-bound states.

### 1. match/
- **bound_levels_0/**: extract the bound levels that contribute to the photoionization cross section, in terms of *2J* and *π*. 
  - *extract_bound_levels_0.py*: input the files that contain the energy and rrtable, the number of electrons of the bound
    configurations, the charge of the core confgurations, and the energy of the ground state of the core configurations in unit of ev.
    Note it is more accurate to use the energy of the ground state of the core with same-n-complex configuration interaction, though
    different-n-complex configuration interaction of the core configurations is used to maximally reproduce the background of BPRM 
    calculation. It outputs the levels in energy ascending order for each symmetry *2J_π*, and the negative and positive levels are 
    separated.
--------
- **create_mesh_1/**: create energy mesh for each bound state level. To delineate the edges, 10 points are uniformly assigned between
  adjacent thresholds. 
  - *extract_trans_awk_1.sh*: collect the transition information for the levels of interest, i.e. the header line for each transition.
  Usually we need to create a symlink that points to a file which contains the levels we are interested in, e.g. 
  `ln -s ../bound_levels_0/0_0_neg bound_levels_0` (see script *run_JJ_Pi.sh* in **match/** directory).
  - *collect_thresh_awk_2.sh*: collect the various thresholds for each level, and output the level index and its thresholds in one 
  single line.
  - *order_thresh_awk_3.sh*: sort the thresholds for each level in ascending order, and append each level with an energy that is 
  105 Ry (or another range of your interest) more than the lowest threshold, and remove other thresholds that are the same as 
  one threshold.
  - *add_mini_diff_awk_4.sh*: append the smallest difference between adjacent thresholds at the end of each line for each level. This
  value is useful when creating energy mesh and 10th of it is used as the increment. So in this way we try to delineat the edges of 
  various transitions.
  - *creat_fine_mesh_5.py*: create an energy mesh for each level, with 10 points in any adjacent shresholds, and 20 points between the 
  last threshold and the maximal energy point.
  - *test_same.awk*: it is called inside of *creat_fine_mesh_5.py* to test the fine mesh whether the adjacent points are the same 
  or not. Usually I do not use it.
  - *run.sh*: show the order of executing the scripts above. It is usually called in a loop to run these steps.
--------
- **generate_PI_2/**: after mesh being generated, the scripts in this folder calculate the photoionization cross section.
  - *fe18_n3.py*: load the existing energy binary file and RRTable binary file and interpret and extrapolate the photoionization 
  cross section for each level in the energy mesh created in **create_mesh_1/**. In this script, we use *fac.InterpCross()* to 
  output the
  data for each transition and then to do the summation over all transitions for each level. We can also use *fac.TotalPICross()* to 
  get the summed result, but in many situtations the energy mesh and number of transitions are large which results in the large memory
  requirement. Thus we abandon it in general.
  - *add_awk.sh*: after *fac.InterpCross()* generates the data for all transitions, it reads the data and sums it up in unit of Mb.
--------
- *run_JJ_Pi.sh*: after the bound levels are extracted in directory **bound_levels_0/**, we are ready to generate the photoionization
cross section for each level in each symmetry category 2J_π.
--------
- **level_identification_3/**: As the levels are sorted in energy-ascending order for each symmetry 2J_π just as in BPRM calculation,
we are ready to just plot the the photoionization cross section of RDW and BPRM. While checking how well they match, we need to make
sure the energy agrees well. In some situations, we need to switch or shift the levels so that they are matched. After finishing matching
the levels, we are ready to print out the level information and find out the configuraiton of each level.
  - *plot_n4_background_1.py*: plot the photoionization cross section of RDW and BPRM and see how well they match with each other. 
  Correction is needed if they don't agree well by switching or shifting to other reasonable levels. File *correct_match_n4* or 
  *correct_match_n3*, where n3 or n4 refers to n=3 or n=4 core configuraitons, contains the information of level switching. These numbers 
  represent the LINE NUMBER of the level in *../bound_levels_0/2J_π_neg* file, assuming the BPRM levels are also written in a file in
  the same format. In the script, we need to set the number of levels in the symmetry of interest in BPRM calculation. Usually the number
  of levels obtained in BPRM calculation is no more than that got from RDW. Required is the number of lines that contain the energies of 
  the core states in the front of each level data set in BPRM calculation. 
  - *level_identification_2.py*: in this script, the file that contains the correction in matching step is needed, and *level_JJ_Pi* is a 
  dictionary contains 2J_π:number_of_levels_in_BPRM.
  - *cat.sh*: a simple script to concatenate the level information into a single file that is needed in **ratio_analysis_4/**.
--------
- **ratio_analysis_4/**: extract the information of the levels whose ratios fall within a range. This script is useful if you want to
  get a rough idea of how well the calculation of BPRM and RDW agrees with each other at the last point, and what kind of levels do well
  and not well. The order of the levels written in files *level_file* and *ratio_file* has to be the same. Usually it is 0_0 (2J_π), 
  0_1, 2_0, 2_1, ..., 16_0, 16_1 for Fe XVII, but of course it can vary as long as they are in the same fashion in these two files.
  - *ratio_configurations.py*: it collects the levels whose ratio <0.5 in 0, >=0.5&<1.5 in 1, >=1.5&<2.5 in 2, etc., the rest of levels 
  in n (in line 8, `ratios = range(n)`).
--------
- **bb_5/**: does the bound-bound top up calculation.
  - *create_e_file.py*: create e-file needed in opacity calculation. In line 7, variable *ind_max_remove* represents the maximum level
    index that bound-quasi-bound transitions should be neglected as they are already included in BPRM. In the *fac.Structure()* part,
    the bound configurations have to be in front of the other quasi-bound configurations. In line 73, it excludes the transitions that are
    from the positive-energy levels, the transitions that have already been included in BPRM stgbb, and the ones that have already been 
    included in bound-free, i.e. resonances due to n=2 core configurations coupled with an outer electron. In list *file_en_454_rest*, 
    the first file has to be energy file, followed by the transition files. These transition files have to share the same energy file,
    otherwise when reading different transition files, levels will be messed up.
  - *create_f_file.py*: creates f-file needed in opacity calculation. The same variable settings as in file *create_e_file.py*.
  
### 2. topup/
In this folder, I will extend the BPRM data to higher energy region using RDW method, add the contribution from other core configurations, and include the other bound state levels that are not included in BPRM calculation. To extend the photoionization cross section tail, we simply add the RDW data at the end of BPRM data for each level. The energy mesh used is divided into two parts. One is the mesh used in BPRM claculation from the lowest ionization threshold to the last point. The other is from the last point in BPRM claculation to 500 Ry of photoelectron energy, and it's created such that 10 points are assigned uniformly between adjacent thresholds of other core configurations that I'm going to describe next. The contribution from other core configurations are added using the mesh that has already considered the thresholds of these core configurations. Lastly, the other bound state levles are included, considering the contribution from all the core configurations used in BPRM and others as described above.

#### 2.1. extract_bprm_tail_n4_0/
- *extract_bprm_0.py*: used to extract the threshold and last point for each level in bprm data for tail-processing. The threshold is used
to determine the highest energy point, i.e. 500 Ry more than the threshold. The last point is used to compare with various thresholds
in order to determine the thresholds that are beyond this point.

#### 2.2. tail_other_targets_1/0-16/ 
- **bound_levels_0/**: only consider the transitions to other core configurations as we want to extract the thresholds due to them, so
  that the energy mesh can be created appropriately.
    - *extract_bound_levels_0.py*: the same as the one in **match/bound_levels_0/**
--------
- **create_mesh_1/**: the filenames of these scripts are the same as those in **match/create_mesh_1/**, but the content can be 
drastically different. 
  - *extract_trans_awk_1.sh*: the same as the one in **match/create_mesh_1/**
  - *collect_thresh_awk_2.sh*: the same as the one in **match/create_mesh_1/**
  - *order_thresh_awk_3.sh*: compared with the one in **match/create_mesh_1/**, line 19 is commented out in the current version, because
  the lowest threshold for each level is stored in **extract_bprm_tail_n4_0/**.
  - *add_mini_diff_awk_4.sh*: the same as the one in **match/create_mesh_1/**
  - *creat_fine_mesh_5.py*: due to the correction in matching step, we first reorder the levels obtained from *add_mini_diff_awk_4.sh*,
  and then determine how to create the energy mesh. If all the thresholds are within the last point of BPRM calculation, then we simply
  assign 400 points between the last point and the point which is 500 Ry above the threshold obtained in **extract_bprm_tail_n4_0/**.
  Otherwise, we find the threshold that just starts to become larger than the last point, and assign 10 points between the last point and
  that threshold, and also 10 points between the following thresholds, and 300 points between the last threshold and the point which is
  500 Ry above the threshold obtained in extract_bprm_tail_n4_0/.
  - *test_same.awk*: the same as the one in **match/create_mesh_1/**
  - *run.sh*: it is slightly different from the one in **match/create_mesh_1/**, in that *creat_fine_mesh_5.py* needs to read some input
  parameters, i.e. *2J* and *π*.
--------
- **generate_PI_2/**: since we are extending the tail, which is due to the core configuraitons that are included BPRM calculation, 
only these core configuraitons are considered. 
  - *fe18_n3.py*: the same as the one in **match/generate_PI_2/**
  - *add_awk.sh*: the same as the one in **match/generate_PI_2/**
--------
- **combine_tail_3/**: attach the RDW tail to BPRM.
  - *combine_tail.py*: since the levels have already been corrected, we are ready to just concatenate the tail to BPRM data. Note, in this 
  script, we can get the ratio of BPRM/RDW at the last point, which can give us a rough idea of how these two calculation compare with 
  each other. Through this ratio, we can find the levels that are doing well and not well using script in **match/ratio_analysis_4/**. To
  activate this option, uncomment out line 34, and comment out line 35.
  - *cat.sh*: simply to concatenate 2J_π_ratio files into one file ratio, which is needed in **match/ratio_analysis_4/**.
--------
- **other_targets_4/**: We are going to add the contribution from other core configurations to the tailed-BPRM data. Before proceeding, 
we need to create a symlink in this directory to '../bound_levels_0/', i.e. `ln -s ../bound_levels_0/`, as the bound level information is
the same.
  - **create_mesh_1/**: extract the energy mesh for each level.
    - *extract_trans_awk_1.sh*: the same as the one in **match/create_mesh_1/**
    - *collect_thresh_awk_2.sh*: the same as the one in **match/create_mesh_1/**
    - *order_thresh_awk_3.sh*: comment out line 19, as the mesh has already been created, now we just need to find the lowest threshold,
    and extract the energy mesh
    - *extract_mesh_4.py*: we take note of the energy index at which the contribution from other core configurations starts to kick
    in in each level and the rest of the energy points are the mesh we need. And there are cases where there are no transitions to these
    core configurations, so we denote it as *skip*. These information will be needed when adding the extra contribution to the tailed-BPRM
    data.
    - *run.sh*: run the first three scripts
  - **generate_PI_2/**: calculate the photoionization cross section.
    - *fe18_n3.py*:  the same as the one in **match/generate_PI_2/**
    - *add_awk.sh*: the same as the one in **match/generate_PI_2/**
  - **combine_other_targets_3/**: 
    - *combine_other_targets.py*: combine the tailed-BPRM data with those in **generate_PI_2/**.
    - *cat.sh*: simply concatenate the these data into one file

#### 2.3. other_levels_2/
We are going to collect all the other bound levels and calculate the photoionization cross section due to all the core configurations included in BPRM calculation and the above top up calculation.
- **bound_levels_0/**: 
  - *extract_bound_levels_0.py*: the same as the one in **match/bound_levels_0/**
  - *extract_other_levels_1.py*: extract all the other bound levels that are not included in BPRM calculation. Note the correction in 
  matching is needed, and *sym_level* is a dictionary containing 2J_π:number_of_levels_in_BPRM.
  - *create_e_file.py*: create the e-file needed in opacity calculation for these bound levels. *ind_base* is the number of bound levels
  included in BPRM calculation, so the unincluded bound levels are indexed based on that number.
--------
- **create_mesh_1/**: 
  - *extract_trans_awk_1.sh*: the same as the one in **match/create_mesh_1/**
  - *collect_thresh_awk_2.sh*: the same as the one in **match/create_mesh_1/**
  - *order_thresh_awk_3.sh*: the same as the one in **match/create_mesh_1/**
  - *add_mini_diff_awk_4.sh*: the same as the one in **match/create_mesh_1/**
  - *creat_fine_mesh_5.py*: compared with the one in **match/create_mesh_1/**, it differs in the way of assigning the points between 
  adjacent thresholds. If the difference is within 10 ev, then 10 points, othewise 20.
  - *split.sh*: split the energy mesh into a few files, each of which contains 1000 levels. This might be helpful when there are so many 
  levels and the number of transitions is huge, so we can split the calculation in a few chunks and run them simultaneously. 1000 can be
  changed to other values.
  - *test_same.awk*: the same as the one in **match/create_mesh_1/**
  - *run.sh*: run the above scripts
--------
- **generate_PI_2/**: 
  - *fe18_n4.py*: it is essentially the same as the one in **match/generate_PI_2/**, but it differs a bit in that it reads an input and 
  the file path changes a bit.
  - *add_awk.sh*:  the same as the one in **match/generate_PI_2/**.
  - *create_run_0.sh*: creates PBS jobs for computation of differents chunks. 1000 should be changed if it is changed in 
  *create_mesh_1/split.sh*.
  - *check_zero_1.py*: remove the first entry that has photoionization cross section of 0.
  - *combine_head_data_2.py*: it needs a file called *head* that contains the same energy of the core configurations as in BPRM 
  calculation, and a file containing the level information, i.e. `ln -s ../bound_levels_0/neg levels`.
----------
- **extract_free_config_3/**:
  - *extract_free_config.py*: it finds the transitions that contribute most of the photoionization cross section for a level in a given
  range (*en_start*, *en_end*). *exp_pi* is a list that contains the exponents of the photoionization cross section.
----------
- **extract_jump_4/**: to analysis the PEC_L_Edge transitions
  - *extract_jump_start_end_1.py*: extract the PEC_L_Edge main transitions for each level. The output file is named as level_exp, e.g.
  100_+01, in which written are the transitions from level 100 with a magnitude of 10^+01 at the first default energy point.
  - *extract_jump_start_end_2.py*: print out the level index, the first and last thresholds for all levels, which are grouped as the 
  principle quantum number of the outer electron.
  - *extract_jump_start_end_3.py*: extract the photoionization cross section near the "last" threhold and 500 Ry.

## 3. fe17_fe18_matched_levels/
In this folder, the photoionization cross section of the matched levels for both FeXVII and FeXVIII are shown. The oscillation at the
right end of BPRM is removed and not included in the opacity calculation.

## 4. fe17_fe18_full_data/
In this folder, the FULL photoionization cross section of the bound levels of FeXVII and FeXVIII are shown in log-log scale.

## III. paper/
In this folder, it contains the scripts that I used to create the plots in the relevant paper (link to be updated).

## IV. Dissertation/
It contains the LaTex source code I used to create my dissertation.
