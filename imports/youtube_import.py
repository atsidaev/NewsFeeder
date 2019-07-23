import requests

from urllib.request import urlopen
from bs4 import BeautifulSoup

from imports.import_base import ImportBase
from common.feed_element import FeedElement
from common.linked_video import LinkedVideo


class YouTubeImport(ImportBase):
    def __init__(self, username):
        self.username = username

    def get_key(self):
        return 'youtube'

    def get_elements(self, count):
        url = 'https://www.youtube.com/user/{0}/videos'.format(self.username)
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        result = []

        videos = soup.find_all('a', {'class': 'yt-uix-tile-link'})

        for v in videos:
            element = FeedElement()
            element.author = soup.find(
                attrs={'name': 'title'}).attrs['content']

            video_address = 'https://www.youtube.com/{0}'.format(
                v.get('href'))
            r = requests.get(video_address)
            element.videos.append(LinkedVideo(r.content))

            video_page = urlopen(video_address)
            video_soup = BeautifulSoup(video_page, 'html.parser')

            element.date = video_soup.find(
                'strong', {'class': 'watch-time-text'}).get_text()
            element.body = video_soup.find(
                'p', id='eow-description').get_text()

            if not element.body:
                element.body = video_soup.find(
                    attrs={'name': 'title'}).attrs['content']

            result.append(element)
            if len(result) >= count:
                break
        return result
