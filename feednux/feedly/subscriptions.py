import json
import requests
from feedly.categories import Category
from feedly.streams import Stream

class Subscription:
    def __init__(self, raw):
        self._raw = raw
        self.title = raw['title']
        self.subscription_id = raw['id']
        self.website = raw['website']
        self.categories = self._parseCategories()

    def _parseCategories(self):
        categories = []

        for category in self._raw['categories']:
            cat = Category(category['id'], category['label'])
            categories.append(cat)

        return categories

    def getContents(self):
        stream = Stream(self.subscription_id)
        entries = stream.getContents()
        return entries

    def getRaw(self):
        return self._raw

    def getTitle(self):
        return self.title

    def getCategories(self):
        return self.categories

    def getWebsite(self):
        return self.website
