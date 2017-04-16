import contextlib
import json
import os
import scrapy
from scrapy.crawler import CrawlerProcess

# start by removing current_seasonals.json (scrapy will append to it)
with contextlib.suppress(FileNotFoundError):
   os.remove('current_seasonals.json')

# Spider Definition
class SeasonalSpider(scrapy.Spider):
   name = 'seasonals'
   start_urls = ['http://deweyspizza.com/menu/from-the-kitchen/']

   def parse(self, response):
      yield \
      {
         'name'  : response.css('#post-72 .h-recent-posts::text').extract(),
         'descr' : response.css('#post-72 .x-recent-posts-content .x-recent-posts-content::text').extract(),
      }

process = CrawlerProcess(
{
   'USER_AGENT'   : 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
   'FEED_FORMAT'  : 'json',
   'FEED_URI'     : "current_seasonals.json"
})

process.crawl(SeasonalSpider)
process.start()

# print the current seasonal specials
with open('current_seasonals.json') as json_file:
   data = json.load(json_file)
   current_name = data[0]['name'][0]
   current_description = data[0]['descr'][0]

# strip escape code \u00a0 at end
current_description = current_description[:-2]

print(current_name)
print(current_description)