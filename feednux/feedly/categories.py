from feedly.streams import Stream
import requests
import json

class Category:
    def __init__(self, category_id, label, description=''):
        self.category_id = category_id
        self.label = label
        self.description = label


    def getContents(self, headers):
        stream = Stream(self.category_id, headers)
        contents = stream.getContents()

        return contents

    def getId(self):
        return self.category_id

    def getLabel(self):
        return self.label
