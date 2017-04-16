# Spider Definition for scraping Dewey's Pizza's website

import contextlib
import os
import scrapy

from scrapy.crawler import CrawlerProcess


class SeasonalSpider(scrapy.Spider):
   name       = 'seasonals'
   start_urls = ['http://deweyspizza.com/menu/from-the-kitchen/']

   def parse(self, response):
      yield \
      {
         'name'  : response.css('#post-72 .h-recent-posts::text').extract(),
         'descr' : response.css('#post-72 .x-recent-posts-content .x-recent-posts-content::text').extract(),
      }

def start():
   #  remove current_seasonals.json if it exists (otherwise scrapy will append to it)
   with contextlib.suppress(FileNotFoundError):
      os.remove('data\\current_seasonals.json')

   process = CrawlerProcess(
   {
      'USER_AGENT'   : 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
      'FEED_FORMAT'  : 'json',
      'FEED_URI'     : "data\\current_seasonals.json"
   })

   # Start scraping
   process.crawl(SeasonalSpider)
   process.start()