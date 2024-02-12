import scrapy


class FilmsSpider(scrapy.Spider):
    name = "films"
    start_urls = ["https://ru.wikipedia.org/wiki/%D0%9A%D0%B0%D1%82%D0%B5%D0%B3%D0%BE%D1%80%D0%B8%D1%8F:%D0%A4%D0%B8%D0%BB%D1%8C%D0%BC%D1%8B_%D0%BF%D0%BE_%D0%B0%D0%BB%D1%84%D0%B0%D0%B2%D0%B8%D1%82%D1%83"]
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"}
    

    def parse(self, response):
        url_begin = 'https://ru.wikipedia.org'

        for selector in response.xpath('//div[@id="mw-pages"]//ul/li'):
            film_url = url_begin + selector.xpath('a/@href').get()
            title = selector.xpath('a/text()').get()
            yield response.follow(film_url, callback=self.parse_film_page, meta={"title": title})

        next_page = response.xpath('//div[@id="mw-pages"]/a[text()="Следующая страница"]/@href').get()
        if next_page:
            yield response.follow(url_begin + next_page, callback=self.parse)
    

    def parse_film_page(self, response):
        film = {}
        film["title"] = response.meta["title"]
        film["genre"] = response.xpath('//table//tr/td/span[@data-wikidata-property-id="P136"]//text()').getall()
        film["director"] = response.xpath('//table//tr/td//span[@data-wikidata-property-id="P57"]//text()').get()
        film["year"] = response.xpath('//table//tr/td//a[contains(@title, "год")]//text()').get()
        film["country"] = response.xpath('//table//tr/td//span[@data-wikidata-property-id="P495"]//a//text()').getall()
        film["IMBD_rating"] = "No rating"
        # film["film_url"] = response.url

        rating_url = response.xpath('//table//tr/td//span[@data-wikidata-property-id="P345"]//a/@href').get()
        if rating_url:
            yield response.follow(rating_url, callback=self.parse_rating_page, headers=self.headers, meta={"item": film})
        else:
            yield film


    def parse_rating_page(self, response):
        film = response.meta["item"]
        film["IMBD_rating"] = response.xpath('//div[@class="sc-3a4309f8-0 bjXIAP sc-69e49b85-1 llNLpA"]//span[@class="sc-bde20123-1 cMEQkK"]/text()').get()
        yield film
