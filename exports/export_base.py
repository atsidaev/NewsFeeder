from common.feed_element import FeedElement

class ExportBase:
	def get_key(self):
		raise NotImplementedError()
	
	def export(self, feed_element):
		raise NotImplementedError()
