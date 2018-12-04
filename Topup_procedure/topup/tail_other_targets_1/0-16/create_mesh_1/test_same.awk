#! /bin/awk -f

#This is to test the fine mesh, whether the points are the same or not

{
#	print "level =", $1 > "OUT"
	for (i = 2; i <= NF-1; i++)
	{
		if ($i == $(i+1))
		{
			print $1, i > "OUT"
		}
	}

}
