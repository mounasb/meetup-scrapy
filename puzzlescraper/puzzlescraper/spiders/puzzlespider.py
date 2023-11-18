import scrapy


class PuzzlespiderSpider(scrapy.Spider):
    name = "puzzlespider"
    start_urls = ["https://ladernierepiece.fr/collections/all"]

    def parse(self, response):
        pass
