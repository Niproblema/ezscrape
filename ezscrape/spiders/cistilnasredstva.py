import scrapy
import re

class CistilnaSredstva(scrapy.Spider):
    name = 'cistlinasredstva'
    start_urls = ['https://www.barjans.si/cistilna-sredstva']

    def parse(self, response):
        for products in response.css('div.grid-items')[0].css('div.item > div.item-body'):
            yield {
                'name': products.css('div.item-title').css('h3').css('a::text').get(),
                'price-eur': products.css('div.item-price').css('span.price::text').get(),
                'link': response.urljoin(products.css('div.item-title').css('h3').css('a').attrib['href']),
                'sifra': re.findall(r'\d+', products.css('small::text').get())[0]
            }
        next_page = response.urljoin(response.css('span.page.next').css('a').attrib['href'])
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)