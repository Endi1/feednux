# TODO Finish implementing all the API, especially thumbnails and images
# TODO figure out how links really work

class Entry:
    """Implementation of the Entry from the feedly API

    Attributes:
    - raw (JSON)
    - entry_id (int)
    - unread (bool)
    - origin (str)
    - title (str)
    - link (str)
    - categories ([str])
    - content (str)
"""

    def __init__(self, raw):
        """
        Arguments
        - raw(JSON) The raw JSON implementation from the Feedly API
        """
        self.raw = raw
        self._buildInstance(self.raw)

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

    def getRaw(self):
        return self.raw
