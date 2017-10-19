from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5 import QtGui
from PyQt5 import QtCore


class ShowStreamWidget(QListWidget):
    """Widget that shows streams as lists
    Attributes:
    - parent (QWidget)
    - local (Local)
    - feed (tuple)
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
        self.itemClicked.connect(self.parent.entryClicked)
        self.setStyleSheet("""
        QListWidget {background-color: #3e4860; color: #D0D4E0; font: 16px bold}
        QListWidget::item {margin: 10px; width: 100%; font-weight: 600}
        QListWidget::item:hover:!pressed {background-color: #6c7a9b}
        QListWidget::item:selected {background-color: #6c7a9b}
        """)
        self.initUI()

    def initUI(self):
        self.stream = self.local.getEntriesForFeed(self.feed)

        for entry in self.stream:
            title = entry[1]
            item = QListWidgetItem(title)
            font = QtGui.QFont()
            font.setBold(True)
            item.setFont(font)
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
