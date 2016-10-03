import pygame, sys
from pygame.locals import *
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


def build_river(temp_map,x,y,river_flag,length,map_visited_temp,num_rivers):
	encountered_visited = 0
	river_length = 0
	count = 0
	row = len(temp_map)
	col = len(temp_map[0])
	if(river_flag == 1):
		while (count < length):
			if coordinate_check(temp_map,x,y)==False:
				x = row - 1
				break
			if map_visited_temp[x][y]==0:
				encountered_visited = 1
				break
			temp_map[x][y] = 3 + 2*num_rivers
			map_visited_temp[x][y]=0
			river_length = river_length + 1
			count = count +1;
			x = x + 1
		
	if(river_flag == 2):
		while (count < length):
			if coordinate_check(temp_map,x,y)==False:
				y = col - 1
				break
			if map_visited_temp[x][y]==0:
				encountered_visited = 1
				break
			temp_map[x][y] = 3 + 2*num_rivers
			map_visited_temp[x][y]=0
			river_length = river_length + 1
			count = count +1;
			y = y+1
	
	if(river_flag == 3):
		while (count < length):
			if coordinate_check(temp_map,x,y)==False:
				x = 0
				break
			if map_visited_temp[x][y]==0:
				encountered_visited = 1
				break
			temp_map[x][y] = 3 + 2*num_rivers
			map_visited_temp[x][y]=0
			river_length = river_length + 1
			count = count +1;
			x = x - 1

	if(river_flag == 4):
		while (count < length):
			if coordinate_check(temp_map,x,y)==False:
				y = 0
				break
			if map_visited_temp[x][y]==0:
				encountered_visited = 1
				break
			temp_map[x][y] = 3 + 2*num_rivers
			map_visited_temp[x][y]=0
			river_length = river_length + 1
			count = count +1;
			y = y - 1	
	print "encountered_visited" + str(encountered_visited) + "\n"
	print "length patch" + str(river_length) + "\n"
	#map_visualize(temp_map)
	return x,y,river_length,encountered_visited

def create_map(row, col, region_length,river_length,river_patch):
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
	num_rivers = 0	
	map_visited = np.full((row,col),1)
	map_visited_temp = np.full((row,col),1)		
	while num_rivers<4:
		entire_river = 0
		temp_map = np.array(map)
		river_flag = 0
		if (num_rivers==0):
			river_flag = 1;
			river_row = 0;
			river_col = random.randint(0,col-1)

		elif (num_rivers==1):
			river_flag = 2;
			river_row = random.randint(0,row-1)
			river_col = 0

		elif (num_rivers==2):
			river_flag = 3;
			river_row = row-1;
			river_col = random.randint(0,col-1)

		elif (num_rivers==3):
			river_flag = 4;
			river_row = random.randint(0,row-1);
			river_col = col-1

		x = river_row
		y = river_col
		j = 0
		while 1:
			if j>0:
				if (random.uniform(0.0,1.0)<=0.25 and river_flag !=3 and river_flag!=1):
					river_flag = 1;
					
				elif (random.uniform(0.0,1.0)<=0.5 and river_flag !=4 and river_flag!=2):
					river_flag = 2;
					
				elif (random.uniform(0.0,1.0)<=0.75 and river_flag !=1 and river_flag!=3):
					river_flag = 3;

				elif (random.uniform(0.0,1.0)<=1.0 and river_flag !=2 and river_flag!=4):
					river_flag = 4;

			j = j + 1
			result = build_river(temp_map,x,y,river_flag,river_patch,map_visited_temp,num_rivers)
			entire_river = entire_river + result[2]
			x = result[0]
			y = result[1]
			if x== 0 or x==row-1 or y==0 or y==col-1:
				if(entire_river<river_length):
					print "Reset due to length constraint"
					#map_visualize(temp_map)
					j = 1
					entire_river = 0
					temp_map = np.array(map)	
					x = river_row
					y = river_col
					map_visited_temp = np.array(map_visited)
					continue
				else:
					print "River done"
					print num_rivers
					num_rivers = num_rivers + 1
					map_visited = np.array(map_visited_temp)
					river_flag = 0;
					map = np.array(temp_map)
					mapToFile(map,"map.txt")
					map_visualize(map)
					break
				
			if result[3]==1:
				print "Reset due to revisit"
				#map_visualize(temp_map)
				j = 1
				entire_river = 0
				temp_map = np.array(map)
				x = river_row
				y = river_col
				map_visited_temp = np.array(map_visited)
				continue
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
	
def map_visualize(map):
	BLUE = (0,0,255)
	BLACK = (0,0,2)
	GREEN = (0,255,0)
	WHITE = (255,255,255)
	TILESIZE = 3
	MAPWIDTH = len(map[0])
	MAPHEIGHT = len(map)

	colors = {0:WHITE, 1:GREEN, 3:BLUE, 2:BLACK, 5:BLUE, 7:BLUE, 9:BLUE}
	pygame.init()
	DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE,MAPHEIGHT*TILESIZE))
	DISPLAYSURF.fill(WHITE)

	for row in xrange(MAPHEIGHT):
		for col in xrange(MAPWIDTH):
			pygame.draw.rect(DISPLAYSURF, colors[map[row][col]], (col*TILESIZE,row*TILESIZE, TILESIZE,TILESIZE))
			pygame.display.update()
	while True:
		for event in pygame.event.get():
			if event.type==QUIT:
				return

 

map = create_map(120,160,15,100,20)
mapToFile(map,"map.txt")
map_visualize(map)