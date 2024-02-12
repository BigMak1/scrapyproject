# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

 
class Film(scrapy.Item):
    film_url = scrapy.Field()
    title = scrapy.Field()
    director = scrapy.Field()
    genre = scrapy.Field()
    year = scrapy.Field()
    country = scrapy.Field()
    rating = scrapy.Field()
