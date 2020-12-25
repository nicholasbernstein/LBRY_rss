#! `env python3`
import urllib
import requests
import json
from datetime import datetime, date, time, timezone


debug = False
now = datetime.now()
URL = 'http://localhost:5279/'
directlink_prefix="https://cdn.lbryplayer.xyz/api/v3/streams/free"

#DATA = '{"method": "claim_list", "params": {"claim_type": "stream", "claim_id": [], "name": [], "is_spent": false, "channel_id": "b6fb38d73b14ce3348841b3f9f66263c5d49f2dd", "resolve": false, "no_totals": false, "include_received_tips": false}}'

Channel_ID="b6fb38d73b14ce3348841b3f9f66263c5d49f2dd"
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
        "include_received_tips": False }
        }

DATA = json.dumps(DATA)
if debug == True:
    print("DATA OUTPUT AS JSON")
    print(DATA)

response = requests.post(url = URL, data = DATA) 

response_dict =  response.json()
def write_raw_js():
    f = open("out.json", "w")
    f.write(json.dumps(response.json(), indent=5))
    f.close()

dict_chaninfo = response_dict['result']['items'][0]['signing_channel']

if debug == True: 
    write_raw_js()
    print(json.dumps(dict_chaninfo['value'], indent=5))

itjs = response_dict['result']['items']

# config
show_title=json.dumps(dict_chaninfo['value']['title'])
show_subtitle="Defending the world from Stupidity since 1979"
contact_name="Nicholas Bernstein"
contact_email="podcast@nicholasbernstein.com"
copyright="2020 Nicholas Bernstein, all rights reserved"
image="https://nicholasbernstein.com/images/me.jpg"
explicit = "No"
lang="en-us"
show_url="https://nicholasbernstein.com/show/"
feed_url="https://nicholasbernstein.com/show_rss.xml"
show_description = json.dumps(dict_chaninfo['value']['description'])
show_description = urllib.parse.quote(show_description, safe=", ", encoding=None, errors=None)
show_thumbnail_url = json.dumps(dict_chaninfo['value']['thumbnail']['url'])
show_thumbnail_url = show_thumbnail_url.strip('\"')
show_category="Technology"
show_category = urllib.parse.quote(show_category, safe=", ", encoding=None, errors=None)
content_type="video/mp4"
pubdt=datetime.now()
publishdate= pubdt.strftime("%A, %d. %B %Y %I:%M%p")
show_keywords = "Technology, linux, devops, IT, career, windows, FreeBSD, kubernetes, software development, open source, oss"
show_keywords = urllib.parse.quote(show_keywords, safe=", ", encoding=None, errors=None)

print('<?xml version="1.0" encoding="UTF-8"?>')
print('<rss version="2.0" xmlns="http://www.w3.org/2005/Atom" xmlns:media="http://search.yahoo.com/mrss/" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">')
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
        file_name=i["value"]["source"]["name"]
        media_type=i["value"]["source"]["media_type"]
        description=urllib.parse.quote(i["value"]["description"],safe=", ", encoding=None, errors=None)
        
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
        #print(json.dumps(i, indent=5))
print("</channel>")    
print("</rss>")    
