import Business
import shapefile_bis as shapefile
import numpy as np

class CensusBlock:
    
    def __init__(self, shape, block_id):
        self.category_counts = {}
        self.business_ids = []
        self.business_ids_set = set()
        self.shape = shape
        self.shape.project_points()
        self.block_id = block_id

    def add(self, business):
        """
        Adds a business to the census block by updating the business id list as well
        as the counts for each category
        """

        # print 'Adding'
        self.business_ids.append(business.get_id())
        self.business_ids_set.add(business.get_id())
        # print self.business_ids
        # print self.business_ids_set
        
        category = business.get_category()
        if not category is None:
            if self.category_counts.has_key(category):
                self.category_counts[category] += 1
            else:
                self.category_counts[category] = 1

    def is_inside(self, business):
        lat, long = business.get_lat_long()
        return self.shape.is_inside(lat, long)

    def get_id(self):
        return self.block_id

    def get_business_ids(self):
        return self.business_ids_set
    def get_counts(self):
        return self.category_counts

    def get_vector(self, categories):
        counts = np.array(np.zeros(len(categories)))
        for i in range(len(categories)):
            if self.category_counts.has_key(categories[i]):
                counts[i] = self.category_counts[categories[i]]
        tot_counts = float(sum(counts))
        if tot_counts:

            vec = np.array([i/tot_counts for i in counts])
        else:
            vec = counts
        return vec

if __name__ == '__main__':
    sf = shapefile.Reader("census2000_blkgrp_nowater/census2000_blkgrp_nowater")
    shapes = sf.shapes()
    print shapes[5].is_inside(1, 1)
