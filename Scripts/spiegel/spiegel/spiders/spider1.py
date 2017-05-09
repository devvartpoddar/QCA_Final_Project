# -*- coding: utf-8 -*-
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

# Generating start urls for scrapy
website = 'http://www.spiegel.de/nachrichtenarchiv/artikel-'
urls = []

for year in range(2000, 2018):
    year_str = str(year)

    for month in range(1, 13):
        # Changing range as per the month involved
        if month % 2 == 1:
            day_range = 32
        else:
            if month == 2:
                if year % 4 == 0:
                    day_range = 29 # Leap years
                else:
                    day_range = 28
            else:
                day_range = 30

        # Changing month string according to month
        month = '0' + str(month) if month < 10 else str(month)

        for day in range(1, day_range):
            day = '0' + str(day) if day < 10 else str(day)

            tmp_url = website + '.'.join([day, month, year_str, 'html'])
            urls.append(tmp_url)


class Spider1Spider(Spider):
    name = "spider1"
    allowed_domains = ["spiegel.de"]
    start_urls = urls

    def parse(self, response):
        articles = response.xpath('//*[@id="content-main"]/div[2]/ul/li')
        for article in articles:
            url = article.xpath('a/@href').extract()[0]
            politik = url.split('/')[1]
            deutsche = url.split('/')[2]
            # Only if Politik to keep the data
            if politik == 'politik' and deutsche == 'deutschland':
                next_page = 'http://www.spiegel.de' + url
                yield Request(next_page, dont_filter=True, callback=self.parse_article)

    def parse_article(self, response):
        date_xpath = '//*[@id="js-article-column"]/div/div[2]/span/time/b[1]'
        date = response.xpath(date_xpath).extract()
        date = re.sub(r'<.+?>', '', date[0])
        date = date.strip().split('.')
        date = '-'.join(date[::-1])

        # category = response.url
        category = response.url
        category = category.split('/')[3]

        # getting the text
        article_xpath = '//*[@id="js-article-column"]/div/p'
        text = response.xpath(article_xpath).extract()
        text = [re.sub(r'<.+?>', '', elem) for elem in text]
        text = [elem.replace('\n', '').replace(',', '').replace('"', '') for elem in text]
        text = ' '.join(text)
        # lemmatising text
        # text = lemmatise_text(text)

        # Exporting output
        output = SpiegelItem()

        output['url'] = response.url
        output['date'] = date
        output['text'] = text
        # output['category'] = category
        # output['source'] = 'spiegel'

        # exporting output
        yield output
