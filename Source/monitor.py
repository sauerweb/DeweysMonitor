import contextlib
import json
import os
import scrapy
import shutil
import tweepy

from scrapy.crawler import CrawlerProcess
from private_credentials import *


#  remove current_seasonals.json if it exists (otherwise scrapy will append to it)
with contextlib.suppress(FileNotFoundError):
   os.remove('output\\current_seasonals.json')

# Spider Definition for scraping Dewey's Pizza's website
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
   'FEED_URI'     : "output\\current_seasonals.json"
})

# Start scraping
process.crawl(SeasonalSpider)
process.start()

# extract the scraped previous seasonal specials
with open('output\\previous_seasonals.json') as json_file:
   data = json.load(json_file)
   previous_name = data[0]['name'][0]

# extract the scraped current seasonal specials
with open('output\\current_seasonals.json') as json_file:
   data = json.load(json_file)
   current_name = data[0]['name'][0]
   current_description = data[0]['descr'][0]

# strip escape code \u00a0 at end
current_description = current_description[:-2]

if previous_name != current_name:
   # setup & send tweet
   auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
   auth.set_access_token(access_token, access_token_secret)
   api = tweepy.API(auth)

   tweet = 'Current special:\n\n' + current_name + ' Pizza' + ' with ' + current_description
   api.update_status(status=tweet)

   # copy the current specials over to the previous specials
   shutil.copyfile('output\\current_seasonals.json', 'output\\previous_seasonals.json')