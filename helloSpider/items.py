# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HellospiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    director = scrapy.Field()
    summary = scrapy.Field()
    url = scrapy.Field()

class VideoItem(scrapy.Item):
    video_id = scrapy.Field()
    video_name = scrapy.Field()
    video_en_name = scrapy.Field()
    video_score = scrapy.Field()
    video_comfrom_platform = scrapy.Field()
    video_comfrom_href = scrapy.Field()
    video_director = scrapy.Field()
    video_actor = scrapy.Field()
    video_figure_info = scrapy.Field()
    video_detail = scrapy.Field()
    category_name = scrapy.Field()
    video_type = scrapy.Field()
    video_area = scrapy.Field()
    video_year = scrapy.Field()
    video_prize = scrapy.Field()
    video_pay_type = scrapy.Field()
    video_pixel = scrapy.Field()
    video_hits = scrapy.Field()
    video_tags = scrapy.Field()
    video_mk_type = scrapy.Field()
    video_watch = scrapy.Field()
    video_language = scrapy.Field()
    video_age = scrapy.Field()
    video_sex = scrapy.Field()