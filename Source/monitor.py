import json
import shutil
import spider
import tweet


spider.start()

# extract the scraped previous seasonal specials
with open('data\\previous_seasonals.json') as json_file:
   data = json.load(json_file)
   previous_name = data[0]['name'][0]

# extract the scraped current seasonal specials
with open('data\\current_seasonals.json') as json_file:
   data = json.load(json_file)
   current_name = data[0]['name'][0]
   current_description = data[0]['descr'][0]

   # strip escape code \u00a0 at end
   current_description = current_description[:-2]

if previous_name != current_name:
   text = 'Current special:\n\n' + current_name + ' Pizza' + ' with ' + current_description
   tweet.send(text)

   # copy the current specials over to the previous specials
   shutil.copyfile('data\\current_seasonals.json', 'data\\previous_seasonals.json')