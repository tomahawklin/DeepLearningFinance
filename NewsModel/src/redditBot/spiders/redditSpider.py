# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.exceptions import CloseSpider
import datetime

class RedditspiderSpider(CrawlSpider):
    name = 'redditSpider'
    allowed_domains = ['https://www.reddit.com/r/worldnews/']
    start_urls = ['http://www.reddit.com/r/worldnews//']
    firstDate = datetime.datetime(2017, 9, 26, 00, 00, 00)

    def parse(self, response):
        s = Selector(response)
        next_link = s.xpath('//span[@class="nextprev"]//a/@href').extract()[0]
        if len(next_link):
            yield self.make_requests_from_url(next_link)
        #Extracting the content using css selectors
        titles = response.css('.title.may-blank::text').extract()
        votes = response.css('.score.unvoted::text').extract()
        times = response.css('time::attr(title)').extract()
       
        #Give the extracted content row wise
        for item in zip(titles,votes,times):
            #create a dictionary to store the scraped info
            scraped_info = {
                'title' : item[0],
                'vote' : item[1],
                'created_at' : item[2]
            }
            if datetime.datetime.strptime(scraped_info['created_at'], '%a %b %d %H:%M:%S %Y UTC') < self.firstDate:
                raise CloseSpider('termination condition met')
            #yield or give the scraped info to scrapy
            yield scraped_info
            
        