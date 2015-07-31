import Business
import CensusBlock
import shapefile_bis as shapefile
import numpy as np
import sys

class City:

    def __init__(self, shape_file):
        self._load_businesses(["SFDataWithCategories1.npy"])#, "SFDataWithCategories2.npy"])
        self._load_census_blocks(shape_file)
        self._populate_census_blocks()

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
        for shape in city.shapes():
            self.census_blocks.append(CensusBlock.CensusBlock(shape))
        print "Done"

    def _populate_census_blocks(self):
        """
        Loop over all the businesses and add them to the correct CensusBlock
        """
        print "\nPopulating census blocks..."
        progress = 1
        for business in self.businesses:
            lat, long = business.get_lat_long()
            if lat == 'NULL' or long == 'NULL':
                continue
            for block in self.census_blocks:
                if block.is_inside(business):
                    block.add(business)
                    break
            progress += 1
            if not progress%100:
                sys.stdout.flush()
                sys.stdout.write("...processing business %s\n"%(progress))
        sys.stdout.flush()
        print "Done"

if __name__ == '__main__':
    sf = City("census2000_blkgrp_nowater/census2000_blkgrp_nowater")