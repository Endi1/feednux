from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QLabel
from PyQt5 import QtCore
import html


class ShowStreamWidget(QListWidget):
    """Widget that shows streams as lists
    Attributes:
    - parent (QWidget)
    - local (Local)
    - stream_url (str)
    """
    def __init__(self, parent, local, feed):
        """
        Arguments
        - parent(QWidget) The parent widget for this widget
        - feedly(Feedly) The global feedly instance
        - stream_id(int) The id of the stream to show
        """
        super().__init__()
        self.feed = feed
        self.stream_url = feed[2]
        self.local = local
        self.parent = parent
        self.itemDoubleClicked.connect(self.parent.entryClicked)
        self.setStyleSheet("""
        QListWidget {background-color: #3e4860; color: #D0D4E0; font: 16px bold}
        QListWidget::item {margin: 2px; width: 100%}
        QListWidget::item:hover:!pressed {background-color: #6c7a9b}
        QListWidget::item:selected {background-color: #6c7a9b}
        """)
        self.initUI()

    def initUI(self):
        self.stream = self.local.getEntriesForFeed(self.feed)

        for entry in self.stream:
            body = entry[1] + "\n" + entry[3]
            item = QListWidgetItem(body)
            item.setData(QtCore.Qt.UserRole, entry)
            self.addItem(item)


class ShowEntryWidget(QWebEngineView):
    """ Render the selected article's HTML

    Attributes:
    - entry_id (int)
    """
    def __init__(self, entry):
        """
        Arguments:
        - entry_id(int) The id of the entry to render
        """
        super().__init__()
        self.entry = entry
        self.initUI()

    def initUI(self):
        link = self.entry[2]
        self.load(QtCore.QUrl(link))
