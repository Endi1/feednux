import requests
import json

from feedly.entries import Entry

# TODO Deal with the continuation thing

class Stream:
    def __init__(self, stream_id, headers={}):
        self.stream_id = stream_id
        self.headers = headers

    def getEntriesIds(self):
        entries = []
        url = 'https://cloud.feedly.com/v3/streams/ids?streamId='+self.stream_id

        response = requests.get(url, headers=self.headers)
        contents = json.loads(response.content)
        entries = contents['ids']

        return entries

    def getContents(self):
        entries = []
        url = 'https://cloud.feedly.com/v3/streams/contents?streamId='+self.stream_id

        response = requests.get(url, headers=self.headers)
        contents = json.loads(response.content)

        for raw_entry in contents['items']:
            entry = Entry(raw_entry)
            entries.append(entry)

        return entries
