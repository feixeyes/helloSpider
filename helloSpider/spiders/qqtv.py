# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from helloSpider.items import HellospiderItem

# scrapy crawl qqtv

class QqtvSpider(CrawlSpider):
    name = 'qqtv'
    allowed_domains = ['v.qq.com' ]
    start_urls = ['http://v.qq.com/x/list/tv']



    # body > div.site_container.container_main > div > div > div.mod_pages > a.page_next

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
        print('Processing detail..' + response.url)
        # container_player > div > div.player_headline.player_headline_mood.cf > div.mod_intro > div.video_base._base > h1 > a
        # leftdown_content > div:nth-child(1) > div.mod_bd > ul > li.mod_summary.intro_item > div.director
        # leftdown_content > div:nth-child(1) > div.mod_bd > ul > li.mod_summary.intro_item > div.video_summary.open > p


        title = response.css('div.mod_intro > div.video_base._base > h1 > a::attr(title)').extract()[0]
        director = response.css('.mod_summary > .director a').extract()[0].strip()
        summary = response.css('.video_summary > .summary').extract()[0]

        item = HellospiderItem()
        item['title'] = title
        item['director'] = director
        item['summary'] = summary
        item['url'] = response.url
        yield item

    # def parse(self, response):
    #     pass


        #detail https://v.qq.com/x/cover/jzhtr2cgy35ejz0.html?
# <strong class="figure_title"><a href="https://v.qq.com/x/cover/lrwweimk8hanlk8.html" target="_blank" title="我的奇妙男友" _stat2="videos:title">我的奇妙男友</a></strong>
