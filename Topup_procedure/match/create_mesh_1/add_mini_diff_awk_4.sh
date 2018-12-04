#! /bin/bash

cat << eof > add_mini_diff.awk
#! /bin/awk -f
BEGIN \
{
 line = 0
 output = "level_thresh_order_mini_diff_4"
}


{	
	line ++
	
	mini_diff = \$3 - \$2
	
	if (mini_diff == 0)
	{
		print line, "mini_diff = 0"
	}
	
	for (i = 3; i <= NF-1; i++)
	{
		if (\$(i+1) - \$i < mini_diff)
		{
			mini_diff = \$(i+1) - \$i
			if (mini_diff == 0)
			{
				print line, "mini_diff = 0"
			}
		}	
	}
	
	\$(NF+1) = mini_diff
	print > output
}

END \
{
	print "line =", line
}
eof

chmod u+x add_mini_diff.awk
./add_mini_diff.awk level_thresh_order_3
