import requests
import json

from feedly.categories import Category
from feedly.subscriptions import Subscription
from feedly.streams import Stream


class Feedly:
    """Main feedly instance.
    Attributes:
    - access_token (string)
    - _headers (dict)
    """

    def __init__(self, access_token):
        """
        Arguments:
        - access_token (string) The access token for the feedly API
        """
        self.access_token = access_token
        self._headers = {
            'Authorization': 'OAuth '+self.access_token
        }

    def getStream(self, stream_id):
        """
        Arguments:
        - stream_id(string): The id of the stream to return
        Returns:
        - stream(Stream): The stream with id=stream_id
        """
        stream = Stream(stream_id, self._headers)
        return stream

    def getSubscriptions(self):
        subscriptions = []
        url = 'https://cloud.feedly.com/v3/subscriptions'

        response = requests.get(url, headers=self._headers)
        subscriptions_raw = json.loads(response.content)

        for raw_subscription in subscriptions_raw:
            sub = Subscription(raw_subscription)
            subscriptions.append(sub)

        return subscriptions

    def getCategories(self):
        categories = []
        url = 'https://cloud.feedly.com/v3/categories'

        response = requests.get(url, headers=self._headers)
        categories_raw = json.loads(response.content)

        for category in categories_raw:
            cat = Category(category['id'], category['label'])
            categories.append(cat)

        return categories

    def getHeaders(self):
        return self._headers
