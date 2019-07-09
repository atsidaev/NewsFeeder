import base64
import os

from exports.export_base import ExportBase

class StupidHtmlExport(ExportBase):
	def __init__(self, filename):
		self.filename = filename

		if not os.path.exists(filename):
			with open(filename, "a+") as f:
				f.write('<head><meta http-equiv="refresh" content="10"></head><body>')

	def get_key(self):
		return "stpd"

	def export(self, feed_element):
		# Doing HTML like it was in 2000!
		with open(self.filename, "a+") as f:
			f.write('<b>%s</b> <i>%s</i>' % (feed_element.date, feed_element.author))
			f.write('<p>%s</p>' % feed_element.body)
			for image in feed_element.images:
				# hack: we assume that only DownloadedImage comes here and we know it's internal structure
				f.write('<img src="data:image/jpeg;base64,%s" />' % base64.b64encode(image.file_contents).decode("utf-8"))
			f.write("<hr />")
