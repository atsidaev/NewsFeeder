import requests
import urllib
import re

from urllib.request import urlopen
from bs4 import BeautifulSoup

from imports.import_base import ImportBase
from common.feed_element import FeedElement
from common.downloaded_image import DownloadedImage
from common.linked_video import LinkedVideo


class VKImport(ImportBase):
    def __init__(self, id):
        self.id = id

    def get_key(self):
        return 'vk'

    def get_elements(self, count):
        url = 'https://vk.com/id{0}'.format(self.id)
        html = urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
        posts = soup.find_all('div', {'class': 'wall_item'})
        result = []

        for p in posts:
            element = FeedElement()
            element.author = p.find(
                'div', {'class': 'wi_author'}).get_text().strip()
            element.date = p.find('a', {'class': 'wi_date'}).get_text()

            if p.select_one('div.wi_body > .pi_text'):
                element.body = p.select_one(
                    'div.wi_body > .pi_text').get_text('\n')
                element.body = element.body.replace('Показать полностью…', '')

            images = p.find_all(
                'div', {'class': 'thumb_map_img'})

            for i in images:
                img_url = i.get('data-src_big')
                match = re.search(r'\.jpg(\|\d*\|\d*)', str(img_url))
                if not match:
                    continue
                img_url = img_url.replace(match.group(1), '')
                r = requests.get(img_url)
                element.images.append(DownloadedImage(r.content))

            links = p.find_all('a', href=True)

            for l in links:
                if re.search(r'/video([\d]+)_([\d]+)', str(l['href'])):
                    match = re.search(r'/video([\d]+)_([\d]+)', str(l['href']))
                    if not match:
                        continue
                    video_address = 'https://vk.com/video{0}_{1}'.format(
                        self.id, match.group(2))
                    r = requests.get(video_address)
                    element.videos.append(LinkedVideo(r.content))
                elif re.search(r'/video-([\d]+)_([\d]+)', str(l['href'])):
                    match = re.search(
                        r'/video-([\d]+)_([\d]+)', str(l['href']))
                    if not match:
                        continue
                    video_address = 'https://vk.com/video-{0}_{1}'.format(
                        match.group(1), match.group(2))
                    r = requests.get(video_address)
                    element.videos.append(LinkedVideo(r.content))

            if p.find('div', {'class': 'pic_body_wrap'}):
                original_body = ""
                original_author = ""
                if p.select_one('div.pi_text:nth-of-type(2)'):
                    original_body = p.select_one(
                        'div.pi_text:nth-of-type(2)').get_text('\n')
                    original_body = original_body.replace(
                        'Показать полностью…', '')

                original_author = p.find(
                    'div', {'class': 'pic_from'}).get_text()

                newElement = FeedElement()
                newElement.author = '{0} shared post by {1}'.format(
                    element.author, original_author)
                newElement.date = element.date
                newElement.body = element.body

                element.author = original_author
                element.body = original_body

                newElement.nested = element
                element = newElement

            result.append(element)
            if len(result) >= count:
                break
        return result
