import scrapy

class ArtworksSpider(scrapy.Spider):
    name = "artworks"
    allowed_domains = ["www.artsy.net"]
    start_urls = ["https://www.artsy.net"]

    custom_settings={
        'FEED_URI':'artworks.json',
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
            yield scrapy.Request(url=absolute_url, callback=self.parse_category_item)

    def parse_category_item(self, response):
        # Extracting the title of the category
        category = response.css("h1.Box-sc-15se88d-0.Text-sc-18gcpao-0.eGPiVT.bTXFzS::text").get()
        artworks = response.css('div[data-test="artworkGridItem"]')

        for artwork in artworks:
            # Extracting artwork name, artist name, price, and place
            artwork_name = artwork.css("div.Box-sc-15se88d-0.Text-sc-18gcpao-0.caIGcn.iVSzqj i::text").get()
            artist_name = artwork.css("div.Box-sc-15se88d-0.Text-sc-18gcpao-0.ilQWRL span[to]::text").get()
            price = artwork.css("div.Box-sc-15se88d-0.Text-sc-18gcpao-0.eXbAnU.bfCidL::text").get()
            place = artwork.css("div.Box-sc-15se88d-0.Text-sc-18gcpao-0.caIGcn.wvERG::text").get()
            image_url= artwork.css("div.Box-sc-15se88d-0.fIeAnl img::attr(src)").get()

            # Extracting artwork date if available
            artwork_info = artwork.css("div.Box-sc-15se88d-0.Text-sc-18gcpao-0.caIGcn.iVSzqj::text").get()
            artwork_info_parts = artwork_info.split(',')
            if len(artwork_info_parts) == 2:
                artwork_date = artwork_info_parts[1].strip()
            else:
                artwork_date = None
            
            yield {
                "category": category,
                "artwork": artwork_name,
                "artist": artist_name,
                "price": price,
                "place": place,
                "artwork_date": artwork_date,
                "image_url": image_url
            }
