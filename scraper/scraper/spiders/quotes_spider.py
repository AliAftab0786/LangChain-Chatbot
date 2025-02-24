import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/"
    ]

    def parse(self, response):
        print("------------------------------------------------")
        print(response.text)
        print("------------------------------------------------")
        title = response.css("title::text").extract_first()
        print(title)
        yield {
            'title': title
        }