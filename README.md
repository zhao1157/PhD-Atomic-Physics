# PhD-Atomic-Physics
This repository includes the main code I wrote for my research in pursuit of an atomic physics PhD degree at the Ohio State University. Note: usually the order of executing the scripts in a folder is the same as the index just before the extension. For example, *a_1.sh*, and *b_2.sh* are in the same directory, so the order of executing them is *a_1.sh* followed by *b_2.sh*. The same rules applies to directories.

## BPRM
- Input files for BPRM:
  - *couple_core_e_0.sh*: in stg2, we need to couple the quantumn numbers **S** and **L** of the target states with those of the outer electron, so this script does this job.
  - *recupd_core_2j_p_0.sh*: in recupd, it can be really tedious to manually input the **2J** and **π** values of the target, so this script collects this information and outputs it appropriately.

-------------------  

- Submit PBS jobs: working on the OSU ASC Unity cluster, I used the following two scripts (mainly the first one) to submit thousands of jobs.
  - *f_bf_submit_1.py*: it divides a certain energy region into a number of sub-ranges, and the input files are created automatically. The folder **error** contains the index of the sub-range which fails due to some reason, and this script can be modified by just a few lines to resubmit those failed ones.
  - *f_bf_submit_nodes_1.py*: this script only differs from the one above by one feature, i.e. requesting a certain node for a job. I implemented this feature after the cluster got into some weird problem that caused my jobs to fail on some nodes.
