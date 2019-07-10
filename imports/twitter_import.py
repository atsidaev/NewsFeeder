import requests
import urllib
from urllib.request import urlopen

from bs4 import BeautifulSoup
from imports.import_base import ImportBase
from common.feed_element import FeedElement
from common.downloaded_image import DownloadedImage


class TwitterImport(ImportBase):
    def get_key(self):
        return 'twitter'

    def get_elements(self, count):
        url = 'https://twitter.com/elonmusk'
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        result = []

        tweets = soup.find_all('link', {'data-item-type': 'tweet'})

        for t in tweets:
            element = FeedElement()
            element.author = t.find('span', {'class': 'username'}).get_text()
            element.body = t.find('p', {"class": 'tweet-text'}).get_text()
            element.date = t.find(
                'a', {'class': 'tweet-timestamp'}).attrs['title']

            result.append(element)
            print(len(result))
            # if len(result) >= count:
            #     break
        return result
