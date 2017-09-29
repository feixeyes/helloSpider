# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from helloSpider.items import HellospiderItem

class IqiyiSpider(CrawlSpider):
    name = 'iqiyi'
    allowed_domains = ['iqiyi.com']
    start_urls = ['http://list.iqiyi.com/']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.mod-page > .a1',)),
             callback="parse_item",
             follow=True),)

    def parse_item(self, response):
        # print('Processing..' + response.url)
        item_links = response.css(".movie-tit > a::attr(href)").extract()
        for a in item_links:
            yield scrapy.Request(a, callback=self.parse_qiyidetail_page)

    def parse_qiyidetail_page(self, response):
        # print('Processing detail..' + response.url)
        try:
            title = response.css(".mod-play-tit > span::text").extract()[0]
            director = response.css(".progInfo_rtp > .type-con > a::attr(title)").extract()[0]
            summary = response.css(".progInfo_intr  > .type-con").extract()[0]

            item = HellospiderItem()
            item['title'] = title
            item['director'] = director
            item['summary'] = summary
            item['url'] = response.url
            yield item
        except Exception as err:
            print('Processing detail..' + response.url)
            print err

