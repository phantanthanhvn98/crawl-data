from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from ..items import ProductsItem
from .utils import parse_gtin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

# RUN SELENIUM IN BACHGROUND
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=chrome_options)

class ProductsSpider(CrawlSpider):
    name = "products"
    allowed_domains = ["cimco.de"]
    start_urls = ["https://cimco.de/de/c/alle-produkte-12173333"]

    rules = (
        #Extract links matching /de/c/{string}-{numbers} to get all prducts of categories
        Rule(LinkExtractor(allow=(r"/de/c/",))),

        #Extract links matching /de/p/{string}-{numbers} parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=(r"/de/p/",)), callback="parse_item", follow=True),
    )

    def get_ful_html(self, link):
        driver.get(link)
        time.sleep(5)
        try:
            shadow_root = driver.find_element(By.CSS_SELECTOR, "#usercentrics-root").shadow_root
            cookie_accept = shadow_root.find_element(By.CSS_SELECTOR, "button[data-testid='uc-accept-all-button']")
            cookie_accept.click()
        except:
            print("[COOKIES] ACCEPTED")
        elements = driver.find_elements(By.CLASS_NAME, "styles_item__header__3rmna")
        for element in elements:
            if "Technische Details" in element.get_attribute("innerHTML"):
                ActionChains(driver).move_to_element(element).click().perform()
                time.sleep(0.5)
        time.sleep(1)
        return driver


    def parse_item(self, response):
        response_ = self.get_ful_html(response.url)
        metadata = response.xpath('//script[contains(text(), "gtin_")]').get()
        product = ItemLoader(item=ProductsItem(), response=response)

        product.add_value("product_name", response.xpath("//h1/text()").get())

        product.add_value("product_url", response.url)

        sku = response.xpath('//div[@class="styles_content__articleNr__fSfEn"]/text()').getall()[-1]
        product.add_value("sku", sku)

        product.add_value("gtin", parse_gtin(metadata))
        
        technical = ''
        for i, tech in enumerate(response_.find_elements(By.XPATH, '//ul[@class="styles_item__data__KCGHy"]/li')):
            li = tech.get_attribute("innerHTML")
            if li == "✓":
                li ="yes"
            if li == "×":
                li = "no"
            prefex  = "##" if i%2 == 0 else "|"
            technical = '{}{}{}'.format(technical, prefex, li)
        product.add_value("technical_details", technical[2:])

        image_urls = ""
        for img in response_.find_elements(By.XPATH, '//div[@class="swiper-wrapper"]/div/img'):
            img_url = img.get_attribute("src")
            if sku.replace(" ", "") in img_url and img_url not in image_urls:
                image_urls = '{},{}'.format(image_urls, img_url)
        product.add_value("image_urls", image_urls[1:])

        description = '\n'.join(response.xpath('//div[@class="styles_item__content__X1CZh"]/p').getall())
        product.add_value("description", description)

        return product.load_item()
