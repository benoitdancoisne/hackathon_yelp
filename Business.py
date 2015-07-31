class Business:

    def __init__(self, header, row):
        self.biz_data = {}
        for i in range(len(header)):
            self.biz_data[header[i]] = row[i]



    def get_id(self):
        return self.biz_data['id']

    def get_lat_long(self):
        lat = self.biz_data['latitude']
        long = self.biz_data['longitude']
        return lat, long

    def get_category(self):
        if self.biz_data.has_key('lvl_cat_name'):
            return self.biz_data['lvl_cat_name']
        else:
            return None

    def get_subcategory(self):
        if self.biz_data.has_key('lvl1_cat_name'):
            return self.biz_data['lvl1_cat_name']
        else:
            return None

if __name__ == '__main__':
    print