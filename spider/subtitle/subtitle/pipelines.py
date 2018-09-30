# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

class SubtitlePipeline(object):
    def process_item(self, item, spider):
        file_name = item['name']
        # print '====file_name:' + file_name
        outBasePath = '/Users/bms/workspace/download/result/'
        if not os.path.exists(outBasePath):
            os.makedirs(outBasePath)

        with open(outBasePath + file_name, 'w') as fp:
            fp.write(item['body'])
            print '====download done: ' + file_name + '==='

        return item
