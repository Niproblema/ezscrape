import scrapy
import re

class CistilnaSredstva(scrapy.Spider):
    name = 'barjansspider'
    start_urls = [
        'https://www.barjans.si/potrosni-material-in-podajalniki',
        'https://www.barjans.si/gostinski-program',
        'https://www.barjans.si/cistilna-sredstva',
        'https://www.barjans.si/pripomocki-za-ciscenje',
        'https://www.barjans.si/zascita-in-osebna-nega',
        'https://www.barjans.si/oprema-franke'
    ]

    def parse(self, response):
        for products in response.css('div.grid-items')[0].css('div.item > div.item-body'):
            yield {
                'name': products.css('div.item-title').css('h3').css('a::text').get(),
                'price-eur': products.css('div.item-price').css('span.price::text').get(),
                'link': response.urljoin(products.css('div.item-title').css('h3').css('a').attrib['href']),
                'sifra': re.findall(r'\d+', products.css('small::text').get())[0]
            }
        next_page_short = response.css('span.page.next').css('a')
        if len(next_page_short):
            yield response.follow(response.urljoin(next_page_short.attrib['href']), callback=self.parse)