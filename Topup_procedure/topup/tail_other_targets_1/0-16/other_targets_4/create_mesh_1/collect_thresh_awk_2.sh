#! /bin/bash

#This script is to collect all the transition threshold into a single file
cat << eof > collect_thresh.awk
#! /bin/awk -f

BEGIN \
{
	output = "level_thresh_2"
}
# First read transitions_1 to store all the bound levels and threshold
FILENAME == "transitions_1" \
{
	if (trans[\$1] == "")
	{
		trans[\$1] = \$5
	}
	else
	{
		trans[\$1] = trans[\$1] "  " \$5
	}
}

#Second read bound_levels_0 to output the threshold in the order of the level 
FILENAME == "bound_levels_0" \
{
	print \$1 " " trans[\$1] > output	
}
eof

chmod u+x collect_thresh.awk

./collect_thresh.awk transitions_1 bound_levels_0
