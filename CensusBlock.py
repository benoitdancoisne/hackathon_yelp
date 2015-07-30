import shapefile_bis as shapefile

class CensusBlock:
    def __init__(self, args):
        self.category_counts = {}

if __name__ == '__main__':
    sf = shapefile.Reader("census2000_blkgrp_nowater/census2000_blkgrp_nowater")
    shapes = sf.shapes()
    print shapes[5].is_inside(1,1)