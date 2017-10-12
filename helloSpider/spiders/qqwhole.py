# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from helloSpider.items import HellospiderItem, VideoItem


# scrapy crawl qqwhole

class QqwholeSpider(CrawlSpider):
    name = 'qqwhole'
    allowed_domains = ['v.qq.com' ]
    category = "";
    start_urls = [#'http://v.qq.com/x/list/tv',#电视机
                  #'http://v.qq.com/x/list/movie',#电影
                  #'http://v.qq.com/x/list/variety',#综艺
                  #'http://v.qq.com/x/list/cartoon',#动漫
                  #'http://v.qq.com/x/list/children',#少儿
                  #'http://v.qq.com/x/list/music',#音乐 短视频
                  #'http://v.qq.com/x/list/doco',#纪录片
                  #'http://v.qq.com/x/list/news',#新闻 短视频
                  # 'http://v.qq.com/x/list/ent',#娱乐 短视频
                  # 'http://v.qq.com/x/list/sports',#体育 短视频
                  #'http://v.qq.com/x/list/games',#游戏 短视频
                  # 'http://v.qq.com/x/list/fun',#搞笑 短视频
                  # 'http://v.qq.com/x/list/kings',#王者荣耀 短视频
                  #'http://v.qq.com/x/list/dv',#微电影
                  # 'http://v.qq.com/x/list/fashion',#时尚 短视频
                  # 'http://v.qq.com/x/list/life',#生活 短视频
                  # 'http://v.qq.com/x/list/baby',#母婴 短视频
                  # 'http://v.qq.com/x/list/auto',#汽车 短视频
                  # 'http://v.qq.com/x/list/tech',#科技 短视频
                  #'http://v.qq.com/x/list/education',#教育
                  # 'http://v.qq.com/x/list/finance',#财经 短视频
                  # 'http://v.qq.com/x/list/house',#房产 短视频
                   'http://v.qq.com/x/list/travel'#旅游 短视频
                ]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.page_next',)),
             callback="parse_item",
             follow=True),)

    def parse_item(self, response):
        print('Processing..' + response.url)
        item_links = response.css('.figure_title > a::attr(href)').extract()
        self.setCategory(response.url)#设置一级分类
        for a in item_links:
            # print a
            yield scrapy.Request(a, callback=self.parse_detail_page)

    def parse_detail_page(self, response):
        # print('Processing detail..' + response.url)
        try:
            name = response.css('div.mod_intro > div.video_base._base > h1 > a::attr(title)').extract()#中文视频名
            en_name = response.css('div.mod_intro > div.video_base._base > h1 > span::text').extract()#英文视频名
            score = response.css('.video_score span::text').extract()#打分
            douban_score = response.css('.video_score > .other_score > .douban_score > .num::text').extract()#豆瓣打分
            imdb_score = response.css('.video_score > .other_score > .imdb_score > .num::text').extract()#imdb打分
            payType = response.css(' div.scroll_top > div > h2 > i::text').extract()#支付方式 付费 vip

            duration = response.xpath('//meta[contains(@itemprop,"duration")]/@content').extract()#视频时长
            director = response.css('.mod_summary > .director a::text').extract()#导演
            actor = response.css('div.mod_bd._starlists > div.mod_people_tabs > div > div > div a::attr(title)').extract()#演员
            detail = response.css('.video_summary > .summary::text').extract()#详情介绍
            area = response.xpath('//meta[contains(@itemprop,"contentLocation")]/@content').extract()#地区
            year = response.xpath('//meta[contains(@itemprop,"uploadDate")]/@content').extract()#上映时间
            hits = response.css('#mod_cover_playnum::text').extract()#点击量
            tags = response.css('div.video_tags._video_tags > a::text').extract()#标签

            language = response.xpath('//meta[contains(@itemprop,"inLanguage")]/@content').extract()#语言
            item = VideoItem()
            item['video_id'] = response.url.split('/')[len(response.url.split('/'))-1].replace('.html','')
            if self.category == "纪录片":
                tags = response.css('#_video_tags_o  > a::text').extract()
                payType = response.css('#mod_follow_act > strong > i > img::attr(alt)').extract()
                name = response.css('div.mod_intro > div.video_base._base > h1 > span::text').extract()
                en_name = ""
            elif self.category == "教育":
                payType = response.css('#mod_follow_act > strong > i > img::attr(alt)').extract()
                name = response.css('div.mod_intro > div.video_base._base > h1 > span::text').extract()
                en_name = ""
            elif self.category in ("音乐","新闻","娱乐","体育","游戏","搞笑","王者荣耀","时尚","生活","母婴","汽车","科技","财经","房产","旅游"):
                name = response.css('div.mod_intro > div.video_base._base > h1 > span::text').extract()
                if len(name) < 1:
                    name = response.css('#mod_desc_video_title_id > h1::text').extract()
                en_name = ""
                tags = response.css('#_video_tags_o > a::text').extract()
                if len(tags) < 1:
                    tags = response.css('div.video_tags > a::text').extract()

            if len(name) > 0 :
                item['video_name'] = name[0].strip()
            else:
                item['video_name'] = response.css('div.mod_intro > div.video_base._base > h1::text').extract()[0].strip()

            if len(en_name) > 0:
                item['video_en_name'] = en_name[0]

            if len(score)>=2:
                item['video_score'] = "".join(score[0:2])
            elif len(score)>0:
                item['video_score'] = score[0]
            else:
                item['video_score'] = 'none'

            if len(douban_score) > 0:
                item['video_douban_score'] = douban_score[0]

            if len(imdb_score) > 0 :
                item['video_imdb_score'] = imdb_score[0]

            item['video_comfrom_platform'] = "腾讯视频"

            item['video_comfrom_href'] = response.url

            if len(duration) > 0 :
                item['video_duration'] = duration[0]

            if len(director) > 0:
                item['video_director'] = director[0].strip()

            if len(actor) > 0:
                item['video_actor'] = " ".join(actor)

            #item['video_figure_info'] =

            if len(detail) > 0:
                item['video_detail'] = detail[0]

            item['category_name'] = self.category

            if len(tags) >= 2:
                if self.category == "综艺" and not tags[1].isdigit():
                    item['video_type'] = " ".join(tags[1:len(tags)])
                elif self.category in ("纪录片","音乐","新闻","娱乐","体育","游戏","搞笑","王者荣耀","时尚","生活","母婴","汽车","科技","财经","房产","旅游"):
                    item['video_type'] = " ".join(tags)
                else :
                    item['video_type'] = " ".join(tags[2:len(tags)])

            if len(area) > 0:
                item['video_area'] = area[0]

            if len(year) > 0:
                item['video_year'] = year[0].split('-')[0]
            if self.category == "微电影" and len(tags) > 1:
                item['video_year'] = tags[1]

            # #item['video_prize'] =

            if len(payType) >0 :
                item['video_pay_type'] = payType[0]

            #item['video_pixel'] =

            if len(hits) > 0:
                item['video_hits'] = hits[0]

            if len(tags) > 0:
                item['video_tags'] = " ".join(tags)

            if self.category=="综艺" and len(payType)>0:
                item['video_mk_type'] = payType[0]
            elif self.category == "纪录片" and len(response.css('div.mod_intro > div.video_base._base > h1::text').extract())>0:
                item['video_mk_type'] = response.css('div.mod_intro > div.video_base._base > h1::text').extract()[0].strip()

            #item['video_watch']
            if len(language) > 0:
                item['video_language'] = language[0]

            if len(tags) > 1 and self.category == "少儿":
                item['video_age'] = tags[1].strip()
            #item['video_sex']
            # item['title'] = title
            # item['director'] = director
            # item['summary'] = summary
            # item['url'] = response.url
            yield item
        except Exception as err:
            print('Processing detail..' + response.url)
            print err


    #设置一级分类名称
    def setCategory(self,url):
        if url.find('movie') > 0 :
            self.category = "电影"
        elif url.find('tv') > 0 :
            self.category = "电视剧"
        elif url.find('variety') > 0:
            self.category = "综艺"
        elif url.find('cartoon') > 0 :
            self.category = "动漫"
        elif url.find('children') > 0 :
            self.category = "少儿"
        elif url.find('music') > 0 :
            self.category = "音乐"
        elif url.find('doco') > 0 :
            self.category = "纪录片"
        elif url.find('news') > 0 :
            self.category = "新闻"
        elif url.find('ent') > 0 :
            self.category = "娱乐"
        elif url.find('sports') > 0 :
            self.category = "体育"
        elif url.find('games') > 0 :
            self.category = "游戏"
        elif url.find('fun') > 0 :
            self.category = "搞笑"
        elif url.find('kings') > 0 :
            self.category = "王者荣耀"
        elif url.find('dv') > 0 :
            self.category = "微电影"
        elif url.find('fashion') > 0 :
            self.category = "时尚"
        elif url.find('life') > 0 :
            self.category = "生活"
        elif url.find('baby') > 0 :
            self.category = "母婴"
        elif url.find('auto') > 0 :
            self.category = "汽车"
        elif url.find('tech') > 0 :
            self.category = "科技"
        elif url.find('education') > 0 :
            self.category = "教育"
        elif url.find('finance') > 0 :
            self.category = "财经"
        elif url.find('house') > 0 :
            self.category = "房产"
        elif url.find('travel') > 0 :
            self.category = "旅游"
