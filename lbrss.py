#!/usr/bin/python3
import urllib
import requests
import json
from datetime import datetime, date, time, timezone

debug = False
now = datetime.now()
URL = 'http://localhost:5279/'
directlink_prefix = "https://cdn.lbryplayer.xyz/api/v3/streams/free"
config_file = "config.json"

def getConfigFromFile(config_file):
    f = open(config_file, "r")
    config = json.load(f)
    f.close()
    return config

config = getConfigFromFile(config_file)

def write_raw_js():
    f = open("out.json", "w")
    f.write(json.dumps(response.json(), indent=5))
    f.close()

def getChanInfoFromLBRYandReturnJSON(URL, Channel_ID):
    DATA = {
        "method": "claim_list",
        "params": {
            "claim_type": "stream",
            "claim_id": [],
            "name": [],
            "is_spent": False,
            "channel_id": Channel_ID,
            "resolve": False,
            "no_totals": False,
            "include_received_tips": False}}

    DATA = json.dumps(DATA)
    if debug == True:
        print("DATA OUTPUT AS JSON")
        print(DATA)

    response = requests.post(url=URL, data=DATA)
    return(response) 

response = getChanInfoFromLBRYandReturnJSON(URL, config['channel_id'])
response_dict =  response.json()
dict_chaninfo = response_dict['result']['items'][0]['signing_channel']

if debug == True:
    write_raw_js()
    print(json.dumps(dict_chaninfo['value'], indent=5))

itjs = response_dict['result']['items']

# derived config 
show_title = json.dumps(dict_chaninfo['value']['title'])
show_description = json.dumps(dict_chaninfo['value']['description'])
show_thumbnail_url = json.dumps(dict_chaninfo['value']['thumbnail']['url'])
show_thumbnail_url = show_thumbnail_url.strip('\"')

pubdt = datetime.now()
publishdate = pubdt.strftime("%A, %d. %B %Y %I:%M%p")

# urlencode things that may include user input that could contain unusual characters that could break things
show_subtitle = urllib.parse.quote(config['show_subtitle'], safe=", ", encoding=None, errors=None)
contact_name = urllib.parse.quote(config['contact_name'], safe=", ", encoding=None, errors=None)
contact_email = urllib.parse.quote(config['contact_email'], safe=", ", encoding=None, errors=None)
copyright = urllib.parse.quote(config['copyright'], safe=", ", encoding=None, errors=None)
image = urllib.parse.quote(config['image'], safe=", ", encoding=None, errors=None)
explicit = config['explicit']
lang = config['lang']
show_url = config['show_url']
feed_url = config['feed_url']
content_type = config['content_type']

show_category = urllib.parse.quote(config['show_category'], safe=", ", encoding=None, errors=None)
show_keywords = urllib.parse.quote(config['show_keywords'], safe=", ", encoding=None, errors=None)
show_description = urllib.parse.quote(show_description, safe=", ", encoding=None, errors=None)
show_title = urllib.parse.quote(show_title, safe=", ", encoding=None, errors=None)

print('<?xml version="1.0" encoding="UTF-8"?>')
print('<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">')
print("<channel>")
print("<title>{}</title>".format(show_title))
print("<link>{}</link>".format(show_url))
print("<image> <url>{}</url> <title>{}</title> <link>{}</link> </image>".format(image, show_title, show_url))
print("<description>{}</description>".format(show_description))
print("<language>{}</language>".format(lang))
print("<copyright>{}</copyright>".format(copyright))
#print("<atom:link href=\"{}\" rel=\"self\" type=\"application/rss+xml\"/>".format(feed_url))
print("<lastBuildDate>{}</lastBuildDate>".format(now))
print("<itunes:owner>")
print("<itunes:author>{}</itunes:author>".format(contact_name))
print("<itunes:email>{}</itunes:email>".format(contact_email))
print("</itunes:owner>")
print("<itunes:summary>\n{}\n</itunes:summary>".format(show_description))
print("<itunes:subtitle>{}</itunes:subtitle>".format(show_subtitle))
print("<itunes:explicit>{}</itunes:explicit>".format(explicit))
print("<itunes:keywords>{}</itunes:keywords>".format(show_keywords))
# the ?type = .jpg is just to trick feed validation
print("<itunes:image href=\"{}?type=.jpg\" />".format(show_thumbnail_url))
print("<itunes:category text=\"{}\"/>".format(show_category))
print("<pubDate>{}</pubDate>".format(pubdt))

failed_items = 0
for i in itjs:
    
    keywords = urllib.parse.quote(", ".join(i["value"]["tags"]), safe=", ", encoding=None, errors=None)
    try:
        file_name = i["value"]["source"]["name"]
        media_type = i["value"]["source"]["media_type"]
        description = urllib.parse.quote(i["value"]["description"],safe=", ", encoding=None, errors=None)
        
        if media_type == content_type :
            link = "{}/{}/{}/{}".format(directlink_prefix, i["name"], i["claim_id"], file_name)
            title = i["normalized_name"]
            title = urllib.parse.quote(title,safe=", ", encoding=None, errors=None)
            reldate = datetime.fromtimestamp(int(i["value"]["release_time"]))
            file_size= i["value"]["source"]["size"]
            duration = i["value"]["video"]["duration"]
            thumbnail_url = i["value"]["thumbnail"]["url"]
            print("<item>")
            print("<title> {} </title>".format(title))
            print("<link>{}</link>".format(link))
            print("<pubDate>{}</pubDate> UTC".format(reldate))
            print("<guid>{}</guid>".format(link))
            print("<description>\n {}\n</description>".format(description))
            print("<enclosure url=\"{}\" length=\"{}\" type=\"{}\"/>".format(link, file_size, media_type ))
            print("<itunes:duration>{}</itunes:duration>".format(duration))
            print("<itunes:summary>{}</itunes:summary>".format(description))
            print("<itunes:image href=\"{}\"/>".format(thumbnail_url))
            print("<itunes:explicit>{}</itunes:explicit>".format(explicit))
            print("<itunes:keywords>{}</itunes:keywords>".format(keywords))
            print("</item>")    
    except:
        #prints the entire json object for so you can find fields
        failed_items = failed_items + 1 
print("</channel>")    
print("</rss>")    
