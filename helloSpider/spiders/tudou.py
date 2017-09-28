# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from helloSpider.items import HellospiderItem

class TudouSpider(CrawlSpider):
    name = 'tudou'
    allowed_domains = ['tudou.com',
                       'youku.com']
    start_urls = ['http://www.tudou.com/category/c_97.html']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.next',)),
             callback="parse_item",
             follow=True),)

    def parse_item(self, response):
        # print('Processing..' + response.url)
        item_links = response.css(".v-meta__title >a::attr(href)").extract()
        for a in item_links:
            yield scrapy.Request("http:"+a, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        print('Processing detail..' + response.url)
        # try:
        #     title = response.css(".mod-play-tit > span").extract()[0]
        #     director = response.css(".progInfo_rtp > .type-con > a::attr(title)").extract()[0]
        #     summary = response.css(".progInfo_intr  > .type-con").extract()[0]
        #
        #     item = HellospiderItem()
        #     item['title'] = title
        #     item['director'] = director
        #     item['summary'] = summary
        #     item['url'] = response.url
        #     yield item
        # except Exception as err:
        #     print('Processing detail..' + response.url)
        #     print err


