import scrapy


class ArtworkcountSpider(scrapy.Spider):
    name = "artworkCount"
    allowed_domains = ["artsy.net"]
    start_urls = ['https://www.artsy.net/collect']

    custom_settings={
        'FEED_URI':'artworkCount.json',
        'FEED_FORMAT' : 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def start_requests(self):
        # Starting point for scraping, URLs to visit
        urls = ["https://www.artsy.net/collect"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_artworks)

    def parse_artworks(self, response):
        # Extracting links to art collection categories
        links = response.css("a.RouterLink__RouterAwareLink-sc-1nwbtp5-0.eeJRiP::attr(href)").getall()
        artworks_links = [link for link in links if link.startswith('/collection')]

        # Visiting each category page to extract artworks
        for link in artworks_links:
            absolute_url = response.urljoin(link)
            print(absolute_url)
            yield scrapy.Request(url=absolute_url, callback=self.parse_category_item)

    def parse_category_item(self, response):
        category = response.css(".Box-sc-15se88d-0.Text-sc-18gcpao-0.eGPiVT.bTXFzS::text").get()
        total_artworks_text = response.css('div.Box-sc-15se88d-0.Text-sc-18gcpao-0.kKwdGZ.JnnaH::text').get()
        total_artworks = int(total_artworks_text.split()[0].replace(',', ''))
        yield {
            "category" : category,
            "total_artworks" : total_artworks
        }        
