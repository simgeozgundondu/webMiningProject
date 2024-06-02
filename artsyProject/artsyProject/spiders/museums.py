import scrapy
import json
import time

class MuseumsSpider(scrapy.Spider):
    name = "museums"
    allowed_domains = ["artsy.net"]
    start_urls = ["https://metaphysics-production.artsy.net/v2"]

    custom_settings = {
        'FEED_URI': 'museums.json',
        'FEED_FORMAT': 'json',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'DOWNLOAD_DELAY': 1,  # wait a minute for request
        'AUTOTHROTTLE_ENABLED': True,  
        'AUTOTHROTTLE_START_DELAY': 1,  # starting delay
        'AUTOTHROTTLE_MAX_DELAY': 10,  # Max delay
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,  # target request number
        'AUTOTHROTTLE_DEBUG': False  # Hata ayıklama için True yapabilirz sonrası içins
    }

    def start_requests(self):
        query = """
        query PartnersSearchQuery(
          $near: String
          $partnerCategories: [String]
          $term: String
          $type: [PartnerClassification]
        ) {
          filterPartners(
            aggregations: [TOTAL]
            defaultProfilePublic: true
            eligibleForListing: true
            near: $near
            partnerCategories: $partnerCategories
            size: 100
            sort: RANDOM_SCORE_DESC
            term: $term
            type: $type
          ) {
            total
            hits {
              text: name
              value: slug
              id
            }
          }
        }
        """
        variables = {
            "near": None,
            "partnerCategories": None,
            "term": "",
            "type": ["INSTITUTION"]
        }
        headers = {'Content-Type': 'application/json'}

        yield scrapy.Request(
            url=self.start_urls[0],
            method='POST',
            headers=headers,
            body=json.dumps({'query': query, 'variables': variables}),
            callback=self.parse_museums
        )

    def parse_museums(self, response):
        data = json.loads(response.text)
        hits = data['data']['filterPartners']['hits']
        for partner in hits:
            museum_contact_url = f"https://www.artsy.net/partner/{partner['value']}/contact"
            museum_description_url = f"https://www.artsy.net/partner/{partner['value']}"

            yield scrapy.Request(url=museum_contact_url, callback=self.parse_museum_contact, meta={'description_url': museum_description_url})
            time.sleep(1)  # wait a second for each museums

    def parse_museum_contact(self, response):
        museum_location = response.css('.Box-sc-15se88d-0.Text-sc-18gcpao-0.cgchZM::text').getall()
        museum_name = response.css('.RouterLink__RouterAwareLink-sc-1nwbtp5-0.dikvRF::text').get()

        if len(museum_location) >= 4:
            country = clean_text(museum_location[3])
            city = clean_text(museum_location[2])
            address = clean_text(museum_location[1])
        else:
            country = city = address = None

        museum_name = clean_text(museum_name)

        description_url = response.meta['description_url']
        yield scrapy.Request(url=description_url, callback=self.parse_museum_description, meta={'museum_name': museum_name, 'country': country, 'city': city, 'address': address})

    def parse_museum_description(self, response):
        museum_name = response.meta['museum_name']
        country = response.meta['country']
        city = response.meta['city']
        address = response.meta['address']
        description = response.css('.Box-sc-15se88d-0.Text-sc-18gcpao-0.bTA-dFE.cgchZM::text').get()

        description = clean_text(description)  # Temizleme işlemi yapılıyor

        yield {
            "museum_name": museum_name,
            "country": country,
            "city": city,
            "address": address,
            "description": description
        }

def clean_text(text):
    if text:
        return text.strip().replace("\r", "").replace("\n", "").replace("\\", "")  # Çift ters eğik çizgiyi kaldırma işlemi (edit text )
    return text
