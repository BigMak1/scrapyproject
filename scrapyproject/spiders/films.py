import scrapy
from scrapyproject.items import Film


class FilmsSpider(scrapy.Spider):
    name = "films"
    start_urls = ["https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83"]

    all_films = []


    def parse(self, response):
        url_begin = 'https://ru.wikipedia.org'
        for selector in response.xpath('//div[@id="mw-pages"]//ul/li'):
            
            film_url = url_begin + selector.xpath('a/@href').get()
            yield response.follow(film_url, callback=self.parse_film_page)

        next_page = url_begin + response.xpath('//div[@id="mw-pages"]/a[text()="Следующая страница"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
    

    def parse_film_page(self, response):
        
        infobox = response.xpath('//table//tr')
        # x_p = '//table//tr/td/span[@data-wikidata-property-id="P136"]//text()'

        yield {
            "title": infobox.xpath('th[@class="infobox-above"]/text()').get(),
            "genre": infobox.xpath('td/span[@data-wikidata-property-id="P136"]//text()').getall(),
            "director": infobox.xpath('td//span[@data-wikidata-property-id="P57"]//text()').get(),
            "year": infobox.xpath('td//a[contains(@title, "год")]//text()').get(),
            "country": infobox.xpath('td//span[@data-wikidata-property-id="P495"]//text()').getall()[1],
            "url": response.url
        }


    # def parse(self, response):
    #     item = Film()
    #     url_begin = 'https://ru.wikipedia.org'
    #     for selector in response.xpath('//div[@id="mw-pages"]//ul/li'):
    #         link = selector.xpath('a/@href').get()
    #         item["film_url"] = url_begin + link
    #         item["title"] = selector.xpath('a/text()').get()
    #         yield item

    #     next_page = url_begin + response.xpath('//div[@id="mw-pages"]/a[text()="Следующая страница"]/@href').get()
    #     if next_page:
    #         yield response.follow(next_page, callback=self.parse)

