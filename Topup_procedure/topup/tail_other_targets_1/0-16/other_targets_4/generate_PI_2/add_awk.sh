#! /bin/awk -f

#How to run this script? ./add_awk.sh time_read=1 file time_read=2 file time_read=3 file
BEGIN \
{
	#count_time_2 = 1
	line_count = 0
	i = 1
	line_count_4 = 0
}


time_read == 1 \
{
	#Read the first line and get the number of points
	num_point = $7
	nextfile
}

#time_read == 2 && NF == 5 && count_time_2 <= num_point \
#{
	#photo_en[count_time_2] = $2
	#count_time_2 ++
#}

time_read == 3 && NF == 5 \
{
	line_count ++
	
	if (line_count <= num_point)
	{
		if (i == 1)
		{
			PI[line_count] = $5	
		}
		else
		{
			PI[line_count] += $5
		}
	}
	else
	{
		line_count = 1
		PI[line_count] += $5
		i ++
	}
}

time_read == 4 \
{
	line_count_4 ++
}

time_read == 4 && line_count_4 == ind \
{
	#Sum the partial data up.
	for (line_count = 1; line_count <= num_point; line_count++)
	{	
		#Print the energy in Ry unit and PI in Mb.
		print $(line_count+1)/13.605693, PI[line_count]*0.01 > "xsectn/" ind
		
	}
	
	nextfile
}


