from common.feed_element import FeedElement

class ImportBase:
	def get_key(self):
		raise NotImplementedError()
	
	def get_elements(self, count):
		raise NotImplementedError()
