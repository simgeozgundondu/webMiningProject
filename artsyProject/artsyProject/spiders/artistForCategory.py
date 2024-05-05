import scrapy

class FinaldenemespiderSpider(scrapy.Spider):
    name = "artistForCategory"
    allowed_domains = ["artsy.net"]
    start_urls = ["https://artsy.net"]

    custom_settings={
        'FEED_URI':'artists_for_category.json',
        'FEED_FORMAT' : 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'}

    def start_requests(self):
        # Define the starting URLs
        urls = [
            "https://www.artsy.net/artists"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_artsy)

    def parse_artsy(self, response):
        # Extract all links
        links = response.css("a.RouterLink__RouterAwareLink-sc-1nwbtp5-0::attr(href)").getall()
         # Select links that start with '/gene'
        gene_links = [link for link in links if link.startswith('/gene')]

        for link in gene_links:
            absolute_url = response.urljoin(link)
             # Create request to go to category page
            yield scrapy.Request(url=absolute_url, callback=self.parse_category_item)

    def parse_category_item(self, response):

        # Extract category title
        category = response.css("h1.Box-sc-15se88d-0.Text-sc-18gcpao-0.bTA-dFE.bTXFzS::text").get()

        # Extract artist names
        artist_names = set(response.css("div.Box-sc-15se88d-0.Flex-cw39ct-0.gaIPKD span[to]::text").getall())
        # Clean unnecessary characters from the names
        artist_names = [name.strip(",") for name in artist_names if name.strip(",")]  
        artist_names = [name.strip() for name in artist_names if name.strip()] 

        if artist_names: 
            yield {
                "url": response.url,
                "category": category,
                "artists": list(set(artist_names))  
            }
