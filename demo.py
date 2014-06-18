#!/usr/local/bin/python
import urllib
# pip install lxml
from lxml import html
from datetime import date

today = date.today()

# follow the base url with the given page param, collect links, and follow next page if available
def follow_page(base_url, page_param, collected):
  data = urllib.urlopen(base_url + page_param)
  root = html.fromstring(data.read())
  # xpath for the speech links on this page
  links = root.xpath(".//ul[@class='entry-list']/li/h3/a")
  for link in links:
    collected.append("http://www.whitehouse.gov" + link.attrib["href"]) # relative links
  # xpath for the link to the next page, if available
  links = root.xpath(".//li[@class='pager-next']/a")
  for link in links:
    next_page = link.attrib["href"].split("?")[1]
    follow_page(base_url, next_page, collected)

# define collected links list here, to be appended for all the monthly archives
collected = []
# the years in question, done the simple way
for year in [2009,2010,2011,2012,2013,2014]:
  for month in [1,2,3,4,5,6,7,8,9,10,11,12]:
    # we don't need to do this in December!
    if year < today.year or (year == today.year and month <= today.month):
      # there's a cleverer way to do this, but I can't remember
      if month < 10: month = "0" + str(month)
      archive_index = "http://www.whitehouse.gov/briefing-room/Speeches-and-Remarks/" + str(year) + "/" + str(month) + "?"
      follow_page(archive_index, "page=0", collected)
for c in collected:
  print c
