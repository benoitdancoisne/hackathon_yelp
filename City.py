import Business
import CensusBlock

class City:

    def __init__(self):
        self._loadBusinesses()
        self._loadCensusBlocks("census2000_blkgrp_nowater/census2000_blkgrp_nowater")
        self._populateCensusBlocks()

    def _loadBusinesses(self):
        self.businesses = []

    def _loadCensusBlocks(self, shapefile):
        self.census_blocks = []

    def _populateCensusBlocks(self):
        for business in self.businesses:
            for block in self.census_blocks:
                if block.isInside(business):
                    block.add(business)
                    break

if __name__ == '__main__':
    print