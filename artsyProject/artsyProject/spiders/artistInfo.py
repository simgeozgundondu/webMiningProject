import scrapy

class ArtistinfoSpider(scrapy.Spider):
    name = "artistInfo"
    allowed_domains = ["artsy.net"]

    start_urls = [
        "https://artsy.net/artists"
    ]
    custom_settings={
        'FEED_URI':'artistsInfo.json',
        'FEED_FORMAT' : 'json',
        'FEED_EXPORT_ENCODING': 'utf-8'}

    def parse(self, response):
        # Extract all artist links on the page
        artist_links = response.css('a.RouterLink__RouterAwareLink-sc-1nwbtp5-0.kHYepE::attr(href)').extract()

        for artist_link in artist_links:
            artist_detail_url = response.urljoin(artist_link)
            yield scrapy.Request(artist_detail_url, callback=self.parse_artist)

    def parse_artist(self, response):
        # Extract artist information from the artist detail page

        # Extract artist name
        artist_name = response.css('h1.Box-sc-15se88d-0.Text-sc-18gcpao-0.bTXFzS::text').get()
        # Extract artist information (nationality and birthdate)
        artist_info = response.css('h2.Box-sc-15se88d-0.Text-sc-18gcpao-0.caIGcn.cCHdck::text').get()
        artist_info_part=artist_info.split(",")

        if len(artist_info_part)==2 :
            artist_nationality=artist_info_part[0].strip()
            artist_date= artist_info_part[1].strip() 
            
        else:
            artist_nationality=artist_info_part[0].strip()

        # Extract artist biography
        artist_bio = response.css('.ReadMore__Container-sc-1bqy0ya-0.dGvePz p::text').get()
        # Extract artworks
        artworks = response.css('.Box-sc-15se88d-0.Text-sc-18gcpao-0.caIGcn.iVSzqj i::text').getall()

        yield {
            'Artist Name': artist_name,
            'Date ': artist_date,
            'Nationality': artist_nationality ,
            'Bio': artist_bio,
            'Artworks':artworks
        }