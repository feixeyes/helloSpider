# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from helloSpider.items import HellospiderItem, VideoItem


# scrapy crawl qqwhole

class QqwholeSpider(CrawlSpider):
    name = 'qqwhole'
    allowed_domains = ['v.qq.com' ]
    start_urls = ['http://v.qq.com/x/list/tv',#电视机
                  'http://v.qq.com/x/list/movie',#电影
                  'http://v.qq.com/x/list/variety',#综艺
                  'http://v.qq.com/x/list/cartoon',#动漫
                  'http://v.qq.com/x/list/children',#少儿
                  'http://v.qq.com/x/list/doco',#纪录片
                  'http://v.qq.com/x/list/news',#新闻 短视频
                  'http://v.qq.com/x/list/ent',#娱乐 短视频
                  'http://v.qq.com/x/list/music',#音乐 短视频
                  'http://v.qq.com/x/list/sports',#体育 短视频
                  'http://v.qq.com/x/list/games',#游戏 短视频
                  'http://v.qq.com/x/list/fun',#搞笑 短视频
                  'http://v.qq.com/x/list/kings',#王者荣耀 短视频
                  'http://v.qq.com/x/list/dv',#微电影
                  'http://v.qq.com/x/list/dv',#微电影
                  'http://v.qq.com/x/list/fashion',#时尚
                  'http://v.qq.com/x/list/life',#生活
                  'http://v.qq.com/x/list/baby',#母婴 短视频
                  'http://v.qq.com/x/list/education',#教育
                  'http://v.qq.com/x/list/finance',#财经 短视频
                  'http://v.qq.com/x/list/house',#房产 短视频
                  'http://v.qq.com/x/list/house'#旅游 短视频
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

            item = VideoItem()
            item['video_id'] +=1
            item['video_name'] = response.css('div.mod_intro > div.video_base._base > h1 > a::attr(title)').extract()[0]
            item['video_en_name'] = response.css('div.mod_intro > div.video_base._base > h1 > a::attr(title)').extract()[0]
            item['video_score'] = response.css().extract()[0]
            item['video_comfrom_platform']
            item['video_comfrom_href']
            item['video_director']
            item['video_actor']
            item['video_figure_info']
            item['video_detail'] = response.css('.video_summary > .summary').extract()[0]
            item['category_name']
            item['video_type']
            item['video_area']
            item['video_year']
            item['video_prize']
            item['video_pay_type']
            item['video_pixel']
            item['video_hits']
            item['video_tags']
            item['video_mk_type']
            item['video_watch']
            item['video_language']
            item['video_age']
            item['video_sex']
            # item['title'] = title
            # item['director'] = director
            # item['summary'] = summary
            # item['url'] = response.url
            yield item
        except Exception as err:
            print('Processing detail..' + response.url)
            print err


