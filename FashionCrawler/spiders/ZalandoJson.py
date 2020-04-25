# -*- coding: utf-8 -*-

# Scrapy Imports
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from FashionCrawler.items import ZalandoArticle

# Other Imports
import json
import os
import urllib



class cd (scrapy.Spider):

    categories = [
        # Women
        'bra', 'womens-clothing-dresses', 'womens-clothing-jackets', 'womens-clothing-jackets-coats',
         'womens-clothing-pullovers-and-cardigans', 'womens-clothing-shirts', 'womens-clothing-blouses-tunics',
         'womens-clothing-jeans', 'womens-clothing-trousers', 'womens-clothing-trousers-overalls-jump-suits',
         'womens-clothing-skirts', 'womens-clothing-underwear', 'womens-clothing-stockings',
           'performance-underwear-women', 'bikini', 'swimsuit',
        # Men
         'men-clothing-shirts', 'mens-clothing-shirts', 'mens-clothing-jackets', 'coats',
         'mens-clothing-pullover-cardigans', 'mens-clothing-jeans', 'mens-clothing-trousers',
         'mens-clothing-suits-combination', 'mens-clothing-suits-waistcoats', 'mens-clothing-suits-trousers',
         'mens-clothing-underwear', 'mens-clothing-socks', 'mens-clothing-swimwear'
    ]

    colors = ['beige','black','blue','brown','gold','green','grey','multicoloured','olive','orange','petrol','pink','purple','red','silver','turquoise','white','yellow']

    baseUrl = 'http://en.zalando.de/'
    mediaBaseString = 'https://mosaic04.ztat.net/vgs/media/catalog-lg'

    name = 'FashionCrawler'
    page_count = 1
    allowed_domains = [baseUrl]

    start_urls = []

    for cat in categories:
        for col in colors:
            # print(baseUrl + cat + "/_" + col)
            start_urls.append(baseUrl + cat + "/_" + col)
            # self.start_urls.append("")


    RESTRICT_CSS = [r'div.z-navicat-header_genders',
                    r'ul.z-navicat-header_categories',
                    r'li.catalogArticlesList_item',
                    r'a.catalogPagination_button-next']
    DENY_REGEX = (r'/myaccount', r'/wishlist', r'/cart')
    # rules = (
    #     Rule(LinkExtractor(deny=DENY_REGEX, restrict_css=RESTRICT_CSS, unique=True), follow=True),
    #     Rule(LinkExtractor(allow=r'.html$', unique=True), callback='parse_item'),
    #     Rule(LinkExtractor(allow=(), restrict_xpaths=('//*[@class="cat_link-8qswi"]/@href',)), callback="parse",
    #          follow=True)
    # )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
            })

    def parse(self, response):
        for url in self.start_urls:
            print ("________"+url)

        articleCount = 0

        sel = Selector(response)
        data_text = sel.xpath('//*[@id="z-nvg-cognac-props"]').extract()
        if data_text:
            data_string = data_text[0]
            data_string = data_string.replace('<script id="z-nvg-cognac-props" type="application/json"><![CDATA[', '')
            data_string = data_string.replace(']]></script>', '')
            data_json = json.loads(data_string)
        else:
            print("Error Loading Json File")

        for article in data_json['articles']:

            print (article)
            zalando_article = ZalandoArticle()

            image_url = self.mediaBaseString + '/' + article['media'][0]['path']
            article_url = self.baseUrl + article['url_key'] + '.html'
            categoryAndColor = response.url.replace("https://en.zalando.de/", "").replace("/", "").split('_')
            category = categoryAndColor[0]
            color = categoryAndColor[1]

            zalando_article['sku'] = article['sku']
            zalando_article['name'] = article['name']
            zalando_article['category'] = category
            zalando_article['color'] = color
            zalando_article['price'] = article['price']['promotional']
            zalando_article['image_url'] = image_url
            zalando_article['article_url'] = article_url
            zalando_article['brand'] = article['brand_name']

            zalando_article.export()

            dir = "Download/Zalando/"  # Standard Dir
            if not os.path.exists(dir + "" + category + "/" + color):
                os.makedirs(dir + "" + category + "/" + color)


            urllib.urlretrieve(image_url, dir + category + "/"+color+ "/" + category + "_" + str(articleCount) + ".jpg")
            articleCount += 1
