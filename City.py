import Business
import CensusBlock
import shapefile_bis as shapefile
import numpy as np
import sys
import operator

from sklearn.cluster import KMeans

class City:

    def __init__(self, shape_file):
        self._load_businesses(["SFDataWithCategories1.npy"])#, "SFDataWithCategories2.npy"])
        self._load_census_blocks(shape_file)
        # self._populate_census_blocks()
        self._populate_census_blocks_from_file('business_to_block_id.csv')

    def _load_businesses(self, biz_files):
        print "\nLoading businesses..."
        self.businesses = []
        header = []
        # limit the number of businesses for testing purpose
        id = 0
        for file in biz_files:
            print "...loading file %s"%(file)
            table = np.load(file)
            for row in table:
                # retrieves header row
                if not row[0].isdigit():
                    header = row
                else:
                    if id < 10:
                        biz = Business.Business(header, row)
                        self.businesses.append(biz)
                        id += 0
        print "Done"

    def _load_census_blocks(self, shape_file):
        """
        Loads a shapefile and create one CensusBlock for each shape
        """
        print "\nLoading census blocks..."
        self.census_blocks = []
        city = shapefile.Reader(shape_file)
        block_id = 0
        for shape in city.shapes():
            block_id += 1
            self.census_blocks.append(CensusBlock.CensusBlock(shape, block_id))
        print "Done"

    def _populate_census_blocks(self):
        """
        Loop over all the businesses and add them to the correct CensusBlock
        """
        output_file = 'business_to_block_id.csv'
        f = open(output_file, 'w')
        print "\nPopulating census blocks..."
        progress = 1
        for business in self.businesses:
            lat, long = business.get_lat_long()
            if lat == 'NULL' or long == 'NULL':
                continue
            for block in self.census_blocks:
                if block.is_inside(business):
                    block.add(business)
                    business_id = business.get_id()
                    block_id = block.get_id()
                    f.write(str(business_id)+','+str(block_id)+'\n')
                    break
            progress += 1
            if not progress%100:
                sys.stdout.flush()
                sys.stdout.write("...processing business %s\n"%(progress))
        sys.stdout.flush()
        print "Done"

    def _populate_census_blocks_from_file(self, file):
        print '\nPopulating census blocks from file...'
        f = open(file, 'r')
        business_to_block_id = dict()
        for line in f:
            line = line[:-1]
            line_vec = line.split(',')
            business_to_block_id[line_vec[0]] = line_vec[1]

        progress = 0
        for business in self.businesses:
            if business.get_id() not in business_to_block_id:
                continue
            block_id_business = business_to_block_id[business.get_id()]
            for block in self.census_blocks:
                block_id = block.get_id()
                if block_id == int(block_id_business):
                    block.add(business)
                    break
            progress += 1
            if not progress%1000:
                sys.stdout.flush()
                sys.stdout.write("...processing business %s\r"%(progress))
        print "\nDone"

    def _get_top_categories(self, num_cat):
        total_counts = {}
        for block in self.census_blocks:
            total_counts.update(block.get_counts())
        top_counts = sorted(total_counts.items(), key=operator.itemgetter(1), reverse=True)[:num_cat]
        return [pair[0] for pair in top_counts]

    def cluster(self, n_clusters, n_categories):
        print "\nClustering into %s clusters..." %n_clusters
        categories = self._get_top_categories(n_categories)
        print "The %s top categories are: " % n_categories
        print categories
        for i in range(len(self.census_blocks)):
            block = self.census_blocks[i]
            if not i:
                data = block.get_vector(categories)
            else:
                data = np.vstack([data, block.get_vector(categories)])
            i += 1
        estimator = KMeans(n_clusters=n_clusters)
        estimator.fit(data)
        print 'estimator = ',estimator
        clusters = estimator.predict(data)
        for i in range(len(self.census_blocks)):
            self.census_blocks[i].set_cluster_id(clusters[i])
        print "Done"

    def generate_viz_data(self):
        f = open('viz_data_part2.csv','w')
        print '\nGenerating visualization data...'
        census_blocks = self.census_blocks

        f.write('block_id,biz_name,category,sub_category,created_time,lat,long,cluster_id\n')

        print 'Number of census_blocks = ', len(census_blocks)
        block_counter = 0
        for block in census_blocks:
            block_counter += 1
            print 'block_counter = ', block_counter
            business_ids = block.get_business_ids()
            for business in self.businesses:
                bus_id = business.get_id()
                if bus_id not in business_ids:
                    continue

                block_id = block.get_id()
                biz_name = business.get_name()
                biz_name = biz_name.replace(',', ' ')
                category = business.get_category()
                sub_category = business.get_subcategory()
                created_time = business.get_created_time()
                lat1, long1 = business.get_lat_long()
                cluster_id = block.get_cluster_id()

                f.write(str(block_id)+','+str(biz_name)+','+str(category)+','+str(sub_category)+','+str(created_time)+','+str(lat1)+','+str(long1)+','+str(cluster_id)+'\n')

if __name__ == '__main__':
    sf = City("census2000_blkgrp_nowater/census2000_blkgrp_nowater")
    sf.cluster(n_clusters=10, n_categories=15)
    sf.generate_viz_data()



