import requests
import urllib

from urllib.request import urlopen
from bs4 import BeautifulSoup

from imports.import_base import ImportBase
from common.feed_element import FeedElement
from common.downloaded_image import DownloadedImage
from common.linked_video import LinkedVideo


class TwitterImport(ImportBase):
    def __init__(self, username):
        self.username = username

    def get_key(self):
        return 'twitter'

    def get_elements(self, count):
        url = 'https://twitter.com/{0}'.format(self.username)
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        tweets = soup.find_all('li', {'data-item-type': 'tweet'})
        result = []

        for t in tweets:
            element = FeedElement()
            element.author = t.find('span', {'class': 'username'}).find('b').get_text()
            element.body = t.find('p', {"class": 'tweet-text'}).get_text()
            element.date = t.find(
                'a', {'class': 'tweet-timestamp'}).attrs['title']

            tweet_id = t.attrs['data-item-id']
            video = t.find(
                'div', {'class': 'PlayableMedia--video'})

            if video is None:
                images = t.find_all(
                    'div', {'class': 'AdaptiveMedia-photoContainer'})
                for i in images:
                    img_url = i.get('data-image-url')
                    r = requests.get(img_url)
                    element.images.append(DownloadedImage(r.content))
            else:
                video_address = 'https://twitter.com/i/status/{0}'.format(tweet_id)
                r = requests.get(video_address)
                element.videos.append(LinkedVideo(r.content))

            # Detect retweet
            if t.find('span', { 'class': 'js-retweet-text' }):
                newElement = FeedElement()
                newElement.author = self.username
                newElement.date = element.date
                newElement.nested = element
                element = newElement

            result.append(element)
            if len(result) >= count:
                break
        return result
