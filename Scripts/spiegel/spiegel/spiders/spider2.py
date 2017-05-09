from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from spiegel.items import SpiegelItem
from spiegel.lemma import lemmatise_text
import re
import csv
import os
import sys
import time
from datetime import datetime

# Generating start urls for scrapy (tagesspiegel)
website = ['http://www.tagesspiegel.de/suchergebnis/?sw=',
    '&search-ressort=',
    '&search-fromday=1&search-frommonth=1&search-fromyear=2013&search-today=9&search-tomonth=3&search-toyear=2017&submit-search=anzeigen']

politik = ['CDU', 'CSU', 'SPD', 'FDP', 'AfD']
wirtschaft = ['wirtschaft']

urls = []

# Create starting URLS
urls.append([website[0] + party + website[1] + '2968' + website[2] for party in politik])
urls.append([website[0] + party + website[1] + '2876' + website[2] for party in wirtschaft])

urls = [item for sublist in urls for item in sublist]

class Spider2Spider(Spider):
    name = "spider2"
    allowed_domains = ["http://www.tagesspiegel.de"]
    start_urls = urls

    def parse(self, response):
        articles = response.xpath('//*[@id="hcf-stage"]/div[4]/div[1]/div[5]/ul/li[1]').extract()
        print(response.body)
        print("--------------------------------------------- \n")
        for article in articles:
            url = article.xpath('a/@href').extract()[0]
            politik = url.split('/')[1]
            print(url)
            # Only if Politik to keep the data
    #         if url:
    #             if politik == 'politik'  or politik == 'wirtschaft':
    #                 article_page = 'http://www.tagesspiegel.de' + url
    #                 yield Request(article_page, dont_filter=True, callback=self.parse_article)
    #
    #     # scraping the next page once over
    #     next_page = response.xpath('//*[@id="hcf-stage"]/div[4]/div[1]/div[6]/ul/li[4]/a/@href')
    #     next_page = next_page.extract()
    #     if next_page:
    #         next_page = "http://www.tagesspiegel.de" + next_page
    #         yield Request(next_page, dont_filter=True, callback=self.parse)
    #
    #
    # def parse_article(self, response):
    #     date_xpath = "//*[@id='19490642']/header/div/time/text()"
    #     date = response.xpath(date_xpath).extract()
    #     date = date.split(" ")[0]
    #     date = date.strip().split('.')
    #     date = '-'.join(date[::-1])
    #
    #     # category = response.url
    #     category = response.url
    #     category = category.split('/')[2]
    #
    #     # getting the text
    #     article_xpath = '//*[@id="19490642"]/div/div[2]/p'
    #     text = response.xpath(article_xpath).extract()
    #     text = [re.sub(r'<.+?>', '', elem) for elem in text]
    #     text = [elem.replace('\n', '').replace(',', '') for elem in text]
    #     text = ' '.join(text)
    #     # lemmatising text
    #     text = lemmatise_text(text)
    #
    #     # Exporting output
    #     output = SpiegelItem()
    #
    #     output['url'] = response.url
    #     output['date'] = date
    #     output['text'] = text
    #     output['category'] = category
    #     output['source'] = 'tagesspiegel'
    #
    #     # exporting output
    #     yield output
