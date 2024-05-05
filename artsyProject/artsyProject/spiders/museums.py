import scrapy

class MuseumsSpider(scrapy.Spider):
    name = "museums"
    allowed_domains = ["artsy.net"]
    start_urls = ["https://www.artsy.net/institutions"]

    def start_requests(self):
        # Starting point for scraping, URLs to visit
        urls = ["https://www.artsy.net/institutions"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_museums)

    def parse_museums(self, response):
    # Extract all museum links on the page
        museums_links = response.css('a.RouterLink__RouterAwareLink-sc-1nwbtp5-0.cJfpRw::attr(href)').getall()
        print("Found {} museum links".format(len(museums_links)))
        for link in museums_links:
            print("Museum Link:", link)
            yield {
                'museum_link': link
            }

# Even though we did everything right, the data did not come from this page https://www.artsy.net/institutions