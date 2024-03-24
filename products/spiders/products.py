from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from ..items import ProductsItem
from .utils import parse_gtin

PAGE = 47

class ProductsSpider(CrawlSpider):
    name = "products"
    allowed_domains = ["cimco.de"]
    start_urls = ["https://cimco.de/de/c/12173333/{}".format(i+1) for i in range(PAGE)]

    rules = (
        #Extract links matching /de/c/{string}-{numbers} to get all prducts of categories
        Rule(LinkExtractor(allow=(r"/de/c/",))),

        #Extract links matching /de/p/{string}-{numbers} parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=(r"/de/p/",)), callback="parse_item", follow=True),
    )


    def parse_item(self, response):
        metadata = response.xpath('//script[contains(text(), "gtin_")]').get()
        product = ItemLoader(item=ProductsItem(), response=response)

        product.add_value("product_name", response.xpath("//h1/text()").get())

        product.add_value("product_url", response.url)

        sku = response.xpath('//div[@class="styles_content__articleNr__fSfEn"]/text()').getall()[-1]
        product.add_value("sku", sku)

        product.add_value("gtin", parse_gtin(metadata))
        
        technical = ''
        for i, li in enumerate(response.xpath('//ul[@class="styles_item__data__KCGHy"]/li').getall()):
            # li = tech.get_attribute("innerHTML")
            if li == "✓":
                li ="yes"
            if li == "×":
                li = "no"
            prefex  = "##" if i%2 == 0 else "|"
            technical = '{}{}{}'.format(technical, prefex, li)
        product.add_value("technical_details", technical[2:])

        image_urls = ""
        for img_url in response.xpath('//div[@class="swiper-wrapper"]/div/img/@src').getall():
            # img_url = img.get_attribute("src")
            if sku.replace(" ", "") in img_url and img_url not in image_urls:
                image_urls = '{},{}'.format(image_urls, img_url)
        product.add_value("image_urls", image_urls[1:])

        description = '\n'.join(response.xpath('//div[@class="styles_item__content__X1CZh"]/p').getall())
        product.add_value("description", description)
        return product.load_item()
