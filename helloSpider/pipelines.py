# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time


class HellospiderPipeline(object):
    def process_item(self, item, spider):
        now = time.strftime('%Y-%m-%d', time.localtime())
        fileName = 'film' + now + '.txt'
        with open(fileName, 'a') as fp:
            fp.write(item['title'].encode('utf8') + '\t')
            fp.write(item['director'].encode('utf8') + '\t')
            fp.write(item['summary'].encode('utf8') + '\t')
            fp.write(item['url'] + '\n\n')
        return item
