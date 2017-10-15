from ..local.Local import Local


class TestClass(object):
    l = Local()

    def test_creation(self):
        assert self.l is not None

    def test_getFeeds(self):
        feeds = self.l.getFeeds()
        assert feeds is not None

    def test_getStream(self):
        feeds = self.l.getFeeds()
        url = feeds[10][2].decode('utf-8')
        stream = self.l.getStream(url)
        assert stream is not None
