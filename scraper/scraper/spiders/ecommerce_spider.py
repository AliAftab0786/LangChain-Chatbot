import scrapy
from scraper.items import ScraperItem

class QuotesSpider(scrapy.Spider):
    name = "ecommerce"
    start_urls = [
        "https://www.hobbycraft.co.uk/home-storage/?sz=200&start=240"
    ]

    def parse(self, response):
        item = ScraperItem()
        all_card = response.xpath("//div[contains(@class, 'col-6') and contains(@class, 'col-sm-4')]/section[contains(@class, 'b-product_tile')]").getall()
        i=1
        for card in all_card:
            title = response.xpath(f"(//a[contains(@class, 'b-product_tile-title') and contains(@class, 'b-product_tile-link')]/text())[{i}]").get()
            price = response.xpath(f"(//p[contains(@class, 'b-price')]/span[(contains(@class, 'b-price-item') or contains(@class, 'm-new')) and not(contains(@class, 'b-price-item m-old'))]/text()[2])[{i}]").get()
            rating = response.xpath(f"(//span[contains(@class, 'b-rating-number')]/text())[{i}]").get()
            
            # Clean the extracted data
            item['title'] = title.strip() if title else None
            item['price'] = price.strip().replace('\n', '').replace('Rs ', '') if price else None
            item['rating'] = rating.strip().replace('\n', '').replace('(', '').replace(')', '') if rating else None
            
            yield item
            i+=1