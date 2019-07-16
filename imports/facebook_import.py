import requests
import urllib
import re

from urllib.request import urlopen
from bs4 import BeautifulSoup

from imports.import_base import ImportBase
from common.feed_element import FeedElement
from common.downloaded_image import DownloadedImage
from common.linked_video import LinkedVideo


class FacebookImport(ImportBase):
    def __init__(self, username):
        self.username = username

    def get_key(self):
        return 'facebook'

    def get_elements(self, count):
        url = 'https://facebook.com/pg/{0}/posts/'.format(self.username)
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        posts = soup.find_all('div', {'class': 'userContentWrapper'})
        result = []

        for p in posts:
            element = FeedElement()
            element.author = p.find('span', {'class': 'fwb'}).get_text()
            element.date = p.find(
                'abbr', {'class': 'livetimestamp'}).attrs['title']
            element.body = p.find(
                'div', {'class': 'userContent'}).get_text()
            if len(element.body) >= 477:
                element.body = element.body[:-len('Ещё')]

            images = p.find_all('div', {'class': 'uiScaledImageContainer'})

            for i in images:
                img_url = i.find('img').get('src')
                r = requests.get(img_url)
                element.images.append(DownloadedImage(r.content))

            links = p.find_all('a', href=True)

            for l in links:
                match = re.search(r'videos/(\d+)/', str(l['href']))
                if not match:
                    continue
                video_id = match.group(1)
                video_address = 'https://facebook.com/{0}/videos/{1}/'.format(
                    self.username, video_id)
                r = requests.get(video_address)
                element.videos.append(LinkedVideo(r.content))

            result.append(element)
            if len(result) >= count:
                break
        return result
