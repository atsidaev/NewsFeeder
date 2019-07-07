import hashlib

from storage.storage_base import StorageBase

class InmemoryStorage(StorageBase):
	def __init__(self):
		self.dict = {}
	
	def add_element(self, service_key, feed_element):
		key = service_key + hashlib.md5(feed_element.body.encode('utf-8')).hexdigest()
		if not key in self.dict:
			self.dict[key] = feed_element
		
	def find_elements(self, service_key, filter_lambda):
		return { k: v for k,v in self.dict.items() if k.startswith(service_key) and filter_lambda(v) }
