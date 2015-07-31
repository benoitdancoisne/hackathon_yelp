import shapefile_bis as shapefile
import pyproj
import random

census_blocks = []
shape_file = "census2000_blkgrp_nowater/census2000_blkgrp_nowater"
city = shapefile.Reader(shape_file)
proj = pyproj.Proj(init='epsg:26943')

output_file = 'blocks_lat_long.csv'
f = open(output_file, 'w')
block_id = 0

for shape in city.shapes():
	block_id += 1
	boundary = shape.points

	random_strength = random.randint(1,100)
	inner_counter = 0

	len_boundary = len(boundary)
	if len_boundary > 10:
		new_shape_points = []
		for i in range(0, len_boundary, int(float(len_boundary)/float(10))):
			new_shape_points.append(boundary[i])
		boundary = new_shape_points

	for (x,y) in boundary:
		mult = float(1200)/float(3937)
		inner_counter += 1
		[long1, lat1] = proj(x*mult, y*mult, inverse=True)
		f.write(str(block_id)+','+str(lat1)+','+str(long1)+','+str(inner_counter)+','+str(random_strength)+'\n')