#! /bin/bash

ln -s ../bound_levels_0/neg bound_levels_0
./extract_trans_awk_1.sh
./collect_thresh_awk_2.sh
./order_thresh_awk_3.sh
./add_mini_diff_awk_4.sh
./creat_fine_mesh_5.py
./split.sh
