import re
import scrapy
from urllib.parse import urljoin


class PuzzlespiderSpider(scrapy.Spider):
    name = "puzzlespider"
    start_urls = ["https://trevell.fr/categorie-produit/puzzle-adulte/"]

    def parse(self, response):
        puzzles = response.xpath("//li[contains(@class, 'daf-product-template')]")

        for puzzle in puzzles:
            product_title = puzzle.xpath(".//h2/text()").get("")
            name = product_title.split("–")[0].replace("Puzzle", "").strip()
            brand = product_title.split("–")[1].strip()
            if match := re.search(
                "(\d+)\s+pièces", product_title.split("–")[2].strip()
            ):
                pieces_nb = match.group(1)
            price = puzzle.xpath(".//bdi/text()").get("").replace(",", ".")
            currency = "€"
            in_stock = not "outofstock" in puzzle.xpath("./@class").get("")
            url = puzzle.xpath(".//a[contains(@class, 'product__link')]/@href").get("")

            item = {
                "name": name,
                "pieces_nb": pieces_nb,
                "brand": brand,
                "price": price,
                "currency": currency,
                "in_stock": in_stock,
                "url": url,
            }

            # yield item

            yield response.follow(
                url=urljoin(response.url, url),
                callback=self.parse_puzzle,
                cb_kwargs={"item": item},
            )

        if next_page := response.xpath("//a[@class='next page-numbers']/@href").get():
            yield response.follow(
                url=urljoin(response.url, next_page), callback=self.parse
            )

    def parse_puzzle(self, response, item):
        item["description"] = (
            response.xpath("string(//div[contains(@class, 'et_pb_wc_description')]//p)")
            .get("")
            .replace("\n", " ")
            .strip()
        )
        yield item
