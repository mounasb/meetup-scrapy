import re
import scrapy
from urllib.parse import urljoin


class PuzzlespiderSpider(scrapy.Spider):
    name = "puzzlespider"
    start_urls = ["https://ladernierepiece.fr/collections/all"]

    def parse(self, response):
        puzzles = response.xpath("//div[contains(@class, 'product-block ')]")

        for puzzle in puzzles:
            name = puzzle.xpath(".//div[@class='product-block__title']/a/text()").get(
                ""
            )
            title = name.split("-")[0].strip()
            if match := re.search("(\d+)\s+pièces", name):
                pieces_nb = match.group(1)
            brand = puzzle.xpath(".//div[@class='product-block__vendor']/text()").get(
                ""
            )
            price = (
                puzzle.xpath(".//div[@class='product-price']/span/text()")
                .get("")
                .replace("€", "")
            )
            currency = "€"
            url = puzzle.xpath(".//div[@class='product-block__title']/a/@href").get("")

            item = {
                "title": title,
                "pieces_nb": pieces_nb,
                "brand": brand,
                "price": price,
                "currency": currency,
                "url": url,
            }

            # yield item
            yield response.follow(
                url=urljoin(response.url, url),
                callback=self.parse_puzzle,
                cb_kwargs={"item": item},
            )

        if next_page := response.xpath("//span[@class='next']/a/@href").get():
            yield response.follow(
                url=urljoin(response.url, next_page), callback=self.parse
            )

    def parse_puzzle(self, response, item):
        item["description"] = response.xpath(
            "string(//div[contains(@class, 'product-description')]/p[1])"
        ).get("")
        yield item
