import requests
import datetime
from urllib.request import urlopen

from bs4 import BeautifulSoup

from imports.import_base import ImportBase
from common.feed_element import FeedElement
from common.downloaded_image import DownloadedImage

class TwitterImport(ImportBase):
	def get_key(self):
		return "twitter"

	def get_elements(self, count):
		url = "https://twitter.com/elonmusk"
		html = urlopen(url)
		soup = BeautifulSoup(html, 'html.parser')
		tweets = soup.find_all('li', { "data-item-type":"tweet" })
		result = FeedElement()

		for t in tweets:
			result.author = "Elon Musk"
			result.body = t.p.get_text().replace('\n', '')
			result.date = t.small.a['title']
		return [ result ]
