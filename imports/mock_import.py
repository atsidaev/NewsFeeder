import lorem
import datetime
import requests

from imports.import_base import ImportBase
from common.feed_element import FeedElement
from common.downloaded_image import DownloadedImage

class MockImport(ImportBase):
	def get_key(self):
		return "mock"

	def get_elements(self, count):
		result = FeedElement()
		result.body = lorem.paragraph()

		r = requests.get("http://www.randomkittengenerator.com/cats/rotator.php", allow_redirects=True)

		result.images.append(DownloadedImage(r.content))
		result.date = datetime.datetime.now()
		result.author = "John Mock"
		return [ result ]
