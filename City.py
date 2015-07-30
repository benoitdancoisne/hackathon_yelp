import Business
import CensusBlock
import shapefile_bis as shapefile

class City:

    def __init__(self, shape_file):
        self._load_businesses()
        self._load_census_blocks(shape_file)
        self._populate_census_blocks()

    def _load_businesses(self):
        self.businesses = []
        #TODO read from file

    def _load_census_blocks(self, shape_file):
        """
        Loads a shapefile and create one CensusBlock for each shape
        """
        self.census_blocks = []
        city = shapefile.Reader(shape_file)
        for shape in city.shapes():
            self.census_blocks.append(CensusBlock.CensusBlock(shape))

    def _populate_census_blocks(self):
        """
        Loop over all the businesses and add them to the correct CensusBlock
        """
        for business in self.businesses:
            for block in self.census_blocks:
                if block.is_inside(business):
                    block.add(business)
                    break

if __name__ == '__main__':
    sf = City("census2000_blkgrp_nowater/census2000_blkgrp_nowater")