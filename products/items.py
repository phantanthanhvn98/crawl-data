# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from itemloaders.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags


def clean_data(value):
    chars_to_move = ["$", "Item"]
    for char in chars_to_move:
        if char in value:
            value = value.replace(char, "")
    return value.strip()

class ProductsItem(scrapy.Item):

    product_name = scrapy.Field(
        input_processor=MapCompose(remove_tags, clean_data),
        output_processor=TakeFirst()
    )
    product_url = scrapy.Field(
        input_processor=MapCompose(remove_tags, clean_data),
        output_processor=TakeFirst()
    )
    sku  = scrapy.Field(
        input_processor=MapCompose(remove_tags, clean_data),
        output_processor=TakeFirst()
    )
    gtin = scrapy.Field(
        input_processor=MapCompose(remove_tags, clean_data),
        output_processor=TakeFirst()

    )
    image_urls = scrapy.Field(
        input_processor=MapCompose(remove_tags, clean_data),
        output_processor=TakeFirst()
    )
    description = scrapy.Field(
        input_processor=MapCompose(remove_tags, clean_data),
        output_processor=TakeFirst()

    )
    technical_details = scrapy.Field(
        input_processor=MapCompose(remove_tags, clean_data),
        output_processor=TakeFirst()
    )