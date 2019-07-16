class FeedElement:
	def __init__(self):
		self.body = None   # text part of the post
		self.images = []   # images from the post
		self.videos = []   # linked and embedded videos from post
		self.author = None # username of full name of author
		self.date = None   # date of post
		self.nested = None # if repost/retweet/resomethingelse, then instance of FeedElement with reposted message is stored here
