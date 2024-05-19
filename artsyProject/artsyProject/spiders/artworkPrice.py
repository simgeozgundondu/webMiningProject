import scrapy


class ArtworkpriceSpider(scrapy.Spider):
    name = "artworkPrice"
    allowed_domains = ["artsy.net"]
    start_urls = ["https://artsy.net"]

    custom_settings={
        'FEED_URI':'artworkPrice.json',
        'FEED_FORMAT' : 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }


    def start_requests(self):
        urls = [
                "https://www.artsy.net/collection/finds-under-1000-dollars",
                "https://www.artsy.net/collection/finds-under-5000-dollars",
                "https://www.artsy.net/collection/finds-under-10000-dollars"
                ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_artworks_price)

    def parse_artworks_price(self, response):
        title = response.css(".Box-sc-15se88d-0.Text-sc-18gcpao-0.eGPiVT.bTXFzS::text").get()
        price_text = response.css(".Box-sc-15se88d-0.Text-sc-18gcpao-0.kKwdGZ.JnnaH::text").get()

        price = int(price_text.strip().split()[0]) if price_text else None

        yield{
            "title" : title,
            "price" : price
        }

