import numpy as np
import random

def coordinate_check(map,x,y):
	row_max = len(map)
	col_max = len(map[0])
	if x<0 or x>=row_max:
		return False
	if y<0 or y>=col_max:
		return False
	return True


def build_river(map,x,y,river_flag):
	river_length = 0

	if(river_flag == 1):
		count = 0
		while (count <= 20 and coordinate_check(map,x,y)):
			map[x][y] = 3
			river_length = river_length + 1
			count = count +1;
			x = x + 1
		
	if(river_flag == 2):
		count = 0
		while (count <= 20 and coordinate_check(map,x,y)):
			
			map[x][y] = 3
			river_length = river_length + 1
			count = count +1;
			y = y+1
	
	if(river_flag == 3):
		count = 0
		while (count <= 20 and coordinate_check(map,x,y)):
			map[x][y] = 3
			river_length = river_length + 1
			count = count +1;
			x = x - 1
			
	if(river_flag == 4):
		count = 0
		while (count <= 20 and coordinate_check(map,x,y)):
			map[x][y] = 3
			river_length = river_length + 1
			count = count +1;
			y = y - 1	

	return map,x,y,river_length

def create_map(row, col, region_length):
	map = np.full((row,col),1)
	map = map.astype(int)
	rand_row = random.randint(0,row)
	rand_col = random.randint(0,col)

	start_row = rand_row - region_length;
	end_row = rand_row + region_length;
	if start_row<0:
		start_row = 0;
	if end_row>(row-1):
		end_row = row-1;

	start_col = rand_col - region_length;
	end_col = rand_col + region_length;
	if start_col<0:
		start_col = 0;
	if end_col>=col:
		end_col = col-1;	

	for i in xrange(start_row, end_row):
		for j in xrange(start_col, end_col):
			if(random.uniform(0.0,1.0)>0.5):
				map[i][j] = 2;
	
	entire_river = 0
	temp_map = map
	river_flag = 0
	if (random.uniform(0.0,1.0)<=0.25 and river_flag !=3):
		river_flag = 1;
		river_row = 0;
		river_col = random.randint(0,col-1)

	elif (random.uniform(0.0,1.0)<=0.5 and river_flag !=4):
		river_flag = 2;
		river_row = random.randint(0,row-1)
		river_col = 0

	elif (random.uniform(0.0,1.0)<=0.75 and river_flag !=1):
		river_flag = 3;
		river_row = row;
		river_col = random.randint(0,col-1)

	elif (random.uniform(0.0,1.0)<=1.0 and river_flag !=2):
		river_flag = 4;
		river_row = random.randint(0,row-1);
		river_col = col

	x = river_row
	y = river_col
	while entire_river<100:
		if (random.uniform(0.0,1.0)<=0.25 and river_flag !=3):
			river_flag = 1;
			river_row = 0;
			river_col = random.randint(0,col-1)

		elif (random.uniform(0.0,1.0)<=0.5 and river_flag !=4):
			river_flag = 2;
			river_row = random.randint(0,row-1)
			river_col = 0

		elif (random.uniform(0.0,1.0)<=0.75 and river_flag !=1):
			river_flag = 3;
			river_row = row;
			river_col = random.randint(0,col-1)

		elif (random.uniform(0.0,1.0)<=1.0 and river_flag !=2):
			river_flag = 4;
			river_row = random.randint(0,row-1);
			river_col = col

		result = build_river(temp_map,x,y,river_flag)
		if result[3] == 0:
			entire_river = 0
			temp_map = map
			x = river_row
			y = river_col
			continue

		entire_river = entire_river + result[3]
		temp_map = result[0]
		x = result[1]
		y = result[2]
	map = temp_map
	return map

def mapToFile(map,name):
	row = len(map)
	col = len(map[0])
	fo = open(name,"w")
	for x in xrange(row):
		string = ""
		for y in xrange(col):
			string = string + str(map[x][y]) + " "
		fo.write(string + "\n")
	fo.close()
	

map = create_map(80,80,10)
mapToFile(map,"map.txt")
