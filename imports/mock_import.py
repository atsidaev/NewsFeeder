import lorem
import datetime
import requests

from imports.import_base import ImportBase
from common.feed_element import FeedElement
from common.downloaded_image import DownloadedImage


class MockImport(ImportBase):
    def get_key(self):
        return "mock"

    def get_elements(self):
        result = []
        for i in range(3):
            element = FeedElement()
            element.body = lorem.paragraph()

            r = requests.get(
                "http://www.randomkittengenerator.com/cats/rotator.php", allow_redirects=True)

            element.images.append(DownloadedImage(r.content))
            element.date = datetime.datetime.now()
            element.author = "John Mock"
            result.append(element)

        return result
