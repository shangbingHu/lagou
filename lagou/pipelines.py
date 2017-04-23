# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json


import pymongo
from pymongo.errors import DuplicateKeyError

class MongoPipeline(object):

    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item



class LagouPipeline(object):
    def process_item(self, item, spider):
        return item


class BigDataToMongodbPipeline(object):

    collection_name = 'bigdata'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'scrapy')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item = dict(item)
        item["_id"] = item["positionId"]
        try:
            if item.has_key('position_desc'):
                self.db[self.collection_name].update({"_id": item["positionId"]}, {"$set": dict(item)})
            else:
                self.db[self.collection_name].insert(dict(item))
        except DuplicateKeyError, e:
            pass
        return item


class BigDataToFilePipeline(object):
    def open_spider(self, spider):
        self.file = open('jobs', 'wb+')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        return item
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
