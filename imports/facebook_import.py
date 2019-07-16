import requests
import urllib
import re
import datetime

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
            element.date = self.get_date(p)
            element.body = p.find(
                'div', {'class': 'userContent'}).get_text()
            element.body = self.remove_see_more(p, element.body, 'Ещё')
            element.body = element.body.replace('…', '')

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

            if self.is_repost(p):
                if p.find(
                        'span', {'class': '_1nb_ fwn fcg'}):
                    original_author = p.find(
                        'span', {'class': '_1nb_ fwn fcg'}).get_text()
                else:
                    original_author = p.find(
                        'span', {'class': 'mbs fwn fcg'}).get_text()

                original_body = p.find(
                    'div', {'class': 'mtm _5pco'}).get_text()
                original_body = self.remove_see_more(p, original_body, 'Ещё')
                original_body = original_body.replace('…', '')

                newElement = FeedElement()
                newElement.author = '{0} shared post by {1}'.format(
                    element.author, original_author)
                newElement.date = element.date
                newElement.body = original_body

                newElement.nested = element
                element = newElement

            result.append(element)
            if len(result) >= count:
                break
        return result

    def remove_see_more(self, post, original, sub):
        return original[:-len(sub)] if original.endswith(sub) else original

    def is_repost(self, post):
        repost_type_one = post.find('div', {'class': 'mtm _5pcm'})
        repost_type_two = post.find('div', {'class': 'mtm _4fzb'})
        repost_type_three = post.find('div', {'class': 'plm _42ef'})
        return repost_type_one or repost_type_two or repost_type_three is not None

    def get_date(self, post):
        date_time = post.find('abbr').get('data-utime')
        date_time = datetime.datetime.fromtimestamp(
            int(date_time)).strftime('%d.%m.%Y %H:%M')
        return date_time
