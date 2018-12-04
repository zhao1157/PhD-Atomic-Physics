#! /bin/bash

#This script is to collect the relevant transitions from ../outfile/fe18a.rr

cat << eof > extract_trans.awk
#! /bin/awk -f
BEGIN \
{
	line_bound_0 = 0
	output = "transitions_1"
	
}

#First read the bound level in file bound_levels_0
FILENAME == "bound_levels_0" \
{
	line_bound_0 ++
	bound_level[\$1] = "get"
}

#Second read the rr table ../outfile/fe17a.rr to collect the relevant transitions
FILENAME == "../outfile/fe18a.rr" && NF == 6 \
{
	if (bound_level[\$1] == "get")
	{
		print > output
	}	
}

END \
{
	print "line_bound_0 = " line_bound_0
	
}


eof

chmod u+x extract_trans.awk

./extract_trans.awk bound_levels_0 ../outfile/fe18a.rr
