from pymongo import mongo_client


class MongoCache:
    def __init__(self, client=None, disk_cache=None):
        self.client = (
            mongo_client.MongoClient('localhost', 27017) if not client else client
        )
        self.db = self.client.video_cache
        self.disk_cache = disk_cache

    def __getitem__(self, key, db_name):
        record = self.db[db_name].find_one({'_id': key})
        if record:
            return record['key']
        elif self.disk_cache and self.disk_cache[key]:
            self[key] = self.disk_cache[key]
            return self.disk_cache[key]
        else:
            raise KeyError('{} cache does not exist'.format(key))

    def __setitem__(self, key, value, db_name):
        self.db[db_name].update({'_id': key}, {'key': value}, upsert=True)

    def length(self, db_name):
        return self.db[db_name].count()


if __name__ == '__main__':
    a = MongoCache()
    print(a.length('video_url'))
