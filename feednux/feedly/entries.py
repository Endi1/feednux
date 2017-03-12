import requests
import json

# TODO Finish implementing all the API, especially thumbnails and images
# TODO figure out how links really work

class Entry:

    def __init__(self, raw=None, entry_id=None):

        if entry_id == None and raw == None:
            self = None
        elif entry_id != None:
            url = 'https://cloud.feedly.com/v3/entries/'+entry_id[11:]
            response = requests.get(url)
            self._buildInstance(json.loads(response.content)[0])
        else:
            self._buildInstance(raw)

    def _buildInstance(self, raw):
        self.raw = raw
        self.entry_id = raw['id']
        self.unread = raw['unread']
        self.origin = raw['origin']
        self.title = raw['title']
        self.link = raw['alternate'][0]['href']
           
        if 'categories' in raw:
            self.categories = raw['categories']
        else:
            self.categories = []

        self._buildContent()

    def _buildContent(self):
        if 'content' in self.raw:
            self.content = self.raw['content']
        else:
            if 'summary' in self.raw:
                self.content = self.raw['summary']
            else:
                self.content = ''

    def getTitle(self):
        return self.title

    def getLink(self):
        return self.link

    def getContent(self):
        return self.content
