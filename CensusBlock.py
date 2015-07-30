import Business
import shapefile_bis as shapefile

class CensusBlock:
    
    def __init__(self):
        self.category_counts = {}
        self.business_ids = []

    def add(self, business):
        self.business_ids.append(business.getId())
        #TODO update counts

    def isInside(self, business):
        return self.shape.is_inside((business.getLatLong()))

if __name__ == '__main__':
    sf = shapefile.Reader("census2000_blkgrp_nowater/census2000_blkgrp_nowater")
    shapes = sf.shapes()
    print shapes[5].is_inside(1,1)