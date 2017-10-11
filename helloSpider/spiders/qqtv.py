# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from helloSpider.items import HellospiderItem

# scrapy crawl qqtv

class QqtvSpider(CrawlSpider):
    name = 'qqtv'
    allowed_domains = ['v.qq.com' ]
    start_urls = ['http://v.qq.com/x/list/movie'#,
                  # 'http://v.qq.com/x/list/tv',
                  # 'http://v.qq.com/x/list/variety',
                  # 'http://v.qq.com/x/list/cartoon',
                  # 'http://v.qq.com/x/list/children',
                  # 'http://v.qq.com/x/list/music',
                  # 'http://v.qq.com/x/list/doco',
                  # 'http://v.qq.com/x/list/news',
                  # 'http://v.qq.com/x/list/ent',
                  # 'http://v.qq.com/x/list/sports',
                  # 'http://v.qq.com/x/list/games',
                  # 'http://v.qq.com/x/list/fun',
                  # 'http://v.qq.com/x/list/kings',
                  # 'http://v.qq.com/x/list/dv',
                  # 'http://v.qq.com/x/list/fashion',
                  # 'http://v.qq.com/x/list/life',
                  # 'http://v.qq.com/x/list/baby',
                  # 'http://v.qq.com/x/list/auto',
                  # 'http://v.qq.com/x/list/tech',
                  # 'http://v.qq.com/x/list/education',
                  # 'http://v.qq.com/x/list/finance',
                  # 'http://v.qq.com/x/list/house',
                  # 'http://v.qq.com/x/list/travel'
                  ]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.page_next',)),
             callback="parse_item",
             follow=True),)

    def parse_item(self, response):
        print('Processing..' + response.url)
        item_links = response.css('.figure_title > a::attr(href)').extract()

        for a in item_links:
            # print a
            yield scrapy.Request(a, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        # print('Processing detail..' + response.url)
        try:
            title = response.css('div.mod_intro > div.video_base._base > h1 > a::attr(title)').extract()[0]
            director = response.css('.mod_summary > .director a::text').extract()[0].strip()
            summary = response.css('.video_summary > .summary::text').extract()[0]

            item = HellospiderItem()
            item['title'] = title
            item['director'] = director
            item['summary'] = summary
            item['url'] = response.url
            yield item
        except Exception as err:
            print('Processing detail..' + response.url)
            print err


