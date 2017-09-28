# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from helloSpider.items import HellospiderItem
import math
import json



class BilibiliSpider(CrawlSpider):
    name = 'bilibili'
    allowed_domains = ['bilibili.com']
    start_urls = ["http://api.bilibili.com/archive_rank/getarchiverankbypartion?type=jsonp&tid=147&pn=2"]

    def parse(self, response):
        data = json.loads(response.text)
        item_count = data["data"]["page"]["count"]
        size = data["data"]["page"]["size"]
        pages = int(math.ceil(item_count / size))
        print pages
        urls = []
        for page in range(pages):
            url = "http://api.bilibili.com/archive_rank/getarchiverankbypartion?type=jsonp&tid=147&pn=" + str(page)
            urls.append(url)
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_item)

    def parse_item(self,response):
        print('Processing..' + response.url)
        data = json.loads(response.text)
        item_links = []
        for i in range(20):
            url = data["data"]["archives"][str(i)]["aid"]
            item_links.append(url)
        for a in item_links:
            yield scrapy.Request("http://www.bilibili.com/video/av" + str(a), callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        print('Processing detail..' + response.url)
        try:
            title = response.css(".v-title > h1::text").extract()[0]
            director = response.css(".usname > .name::text").extract()[0]
            summary = response.css(".v_desc::text").extract()[0]

            item = HellospiderItem()
            item['title'] = title
            item['director'] = director
            item['summary'] = summary
            item['url'] = response.url
            yield item
        except Exception as err:
            print('Processing detail..' + response.url)
            print err





