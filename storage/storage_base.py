from common.feed_element import FeedElement

# Persistency level for imported/exported elements.


class StorageBase:
    def add_element(self, service_key, feed_element):
        raise NotImplementedError()

    def find_elements(self, service_key, filter_lambda):
        raise NotImplementedError()

    def find_element(self, service_key, filter_lambda):
        result = self.find_element(service_key, filter_lambda)
        if len(result) > 0:
            return result[0]
        return None
