import scrapy


class PuzzlespiderSpider(scrapy.Spider):
    name = "puzzlespider"
    start_urls = ["https://trevell.fr/categorie-produit/puzzle-adulte/"]

    def parse(self, response):
        pass
