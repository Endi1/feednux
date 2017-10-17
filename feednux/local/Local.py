import listparser
import datetime
import time
import sqlite3
from pathlib import Path
import feedparser
import re
import html


def cleanHtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    cleantext = html.unescape(cleantext)
    return cleantext


class Local:
    def __init__(self):
        self.home = str(Path.home())
        self.conn = sqlite3.connect(self.home + "/.feednux.db")
        self.cursor = self.conn.cursor()

    def parseOpml(self, filepath):
        with open(filepath, encoding='utf-8') as f:
            file_data = f.read()
            self._opml_result = listparser.parse(file_data)
            self.__saveToDB()

    def __saveToDB(self):
        items = []

        for item in self._opml_result.feeds:
            title = item.title.encode('utf-8')
            url = item.url.encode('utf-8')

            self.cursor.execute("""SELECT * FROM feeds
            WHERE title=?""", (title,))

            if self.cursor.fetchone() is None:
                items.append((None, title, url))

        self.cursor.executemany("""INSERT INTO feeds VALUES (?, ?, ?)""",
                                items)
        self.conn.commit()

    def getFeeds(self):

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS feeds
        (id integer primary key not null ,
        title text not null,
        url text not null)""")

        feeds = []
        self.cursor.execute("SELECT * FROM feeds")
        feeds = self.cursor.fetchall()

        return feeds

    def addFeed(self, title, url):
        self.cursor.execute("""SELECT * FROM feeds WHERE title=?""", title)

        if self.cursor.fetchone() is None:
            self.cursor.execute("""INSERT INTO feeds
            VALUES (?, ?, ?)""", (None, title, url))

    def cacheEntriesFromFeed(self, feed):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS entries
        (id integer primary key not null ,
        title text not null,
        url text not null,
        description text,
        published_at integer not null,
        feed_id integer not null,
        foreign key(feed_id) references feeds(id))""")

        stream_url = feed[2]
        stream_id = feed[0]
        stream = feedparser.parse(stream_url.decode('utf-8'))
        entries = stream.entries
        uncached_entries = []

        for entry in entries:
            now = datetime.datetime.now()
            title = entry.title
            url = entry.link
            description = cleanHtml(entry.summary)
            published_at = entry.get('published_parsed',
                                     datetime.datetime.timetuple(now))
            published_unix = time.mktime(published_at)

            self.cursor.execute("""SELECT *
            FROM entries
            WHERE title=? AND feed_id=?""", (title, stream_id))

            if self.cursor.fetchone() is None:
                uncached_entries.append((None, title, url, description,
                                         published_unix,
                                         feed[0]))

        self.cursor.executemany("INSERT INTO entries VALUES (?,?,?,?,?,?)",
                                uncached_entries)
        self.conn.commit()
        return

    def getEntriesForFeed(self, feed):
        self.cacheEntriesFromFeed(feed)
        self.cursor.execute("SELECT * FROM entries WHERE feed_id=?",
                            (feed[0],))
        entries = self.cursor.fetchall()
        return entries
