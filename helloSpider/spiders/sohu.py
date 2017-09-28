# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from helloSpider.items import HellospiderItem

class SohuSpider(CrawlSpider):
    name = 'sohu'
    allowed_domains = ['so.tv.sohu.com']
    start_urls = ['http://so.tv.sohu.com/list_p1101_p2_p3_p4_p5_p6_p7_p8_p9_p101_p11_p12_p13.html']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.page_next',)),
             callback="parse_item",
             follow=True),)

    def parse_item(self, response):
        print('Processing..' + response.url)
        item_links = response.css('.figure_title > a::attr(href)').extract()

        for a in item_links:
            yield scrapy.Request(a, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        title = response.css('div.mod_intro > div.video_base._base > h1 > a::attr(title)').extract()[0]
        director = response.css('.mod_summary > .director a').extract()[0].strip()
        summary = response.css('.video_summary > .summary').extract()[0]

        item = HellospiderItem()
        item['title'] = title
        item['director'] = director
        item['summary'] = summary
        item['url'] = response.url
        yield item

