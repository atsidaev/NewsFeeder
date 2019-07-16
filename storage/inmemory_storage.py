import hashlib

from storage.storage_base import StorageBase


class InmemoryStorage(StorageBase):
    def __init__(self):
        self.dict = {}

    def add_element(self, service_key, feed_element):
        body = (feed_element.body if feed_element.body else "") + \
            (feed_element.nested.body if feed_element.nested else "") + \
            feed_element.date + feed_element.author
        key = service_key + hashlib.md5(body.encode('utf-8')).hexdigest()
        if not key in self.dict:
            self.dict[key] = feed_element

    def find_elements(self, service_key, filter_lambda):
        return {k: v for k, v in self.dict.items() if k.startswith(service_key) and filter_lambda(v)}
