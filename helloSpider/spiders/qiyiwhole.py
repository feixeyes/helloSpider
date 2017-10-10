# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from helloSpider.items import HellospiderItem

class QiyiwholeSpider(CrawlSpider):
    name = 'iqiyiwhole'
    allowed_domains = ['iqiyi.com']
    start_urls = ['http://www.iqiyi.com']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('a',)),
             callback="parse_item",
             follow=True),)

    def parse_item(self, response):
        # print('Processing..' + response.url)

        try:
            if len(response.css(".mod-play-tit > span").extract())!=0:
                print('saving data'+response.url)
                title = response.css(".mod-play-tit > span::text").extract()[0]
                # director = response.css(".progInfo_rtp > .type-con > a::attr(title)").extract()[0]
                # summary = response.css(".progInfo_intr  > .type-con").extract()[0]

                item = HellospiderItem()
                item['title'] = title
                # item['director'] = director
                # item['summary'] = summary
                item['url'] = response.url
                yield item
        except Exception as err:
            print('Processing detail..' + response.url)
            print err

