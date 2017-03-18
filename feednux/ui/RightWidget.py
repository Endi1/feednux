from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QWidget, QListWidget, QListWidgetItem, QHBoxLayout
from PyQt5 import QtCore
from config import access_token

from feedly.entries import Entry

class ShowStreamWidget(QListWidget):
    """Widget that shows streams as lists
    
    Attributes:
    - parent (QWidget)
    - feedly (Feedly)
    - stream_id (int)
    - stream (Stream)
    """
    
    def __init__(self, parent, feedly, stream_id):
        """
        Arguments
        - parent(QWidget) The parent widget for this widget
        - feedly(Feedly) The global feedly instance
        - stream_id(int) The id of the stream to show
        """
        super().__init__()
        self.stream_id = stream_id
        self.feedly = feedly
        self.parent = parent
        self.itemDoubleClicked.connect(self.parent.entryClicked)
        self.initUI()

    def initUI(self):
        self.stream = self.feedly.getStream(self.stream_id)
        contents = self.stream.getContents()

        for entry in contents:
            item = QListWidgetItem(entry.getTitle())
            item.setData(QtCore.Qt.UserRole, entry)
            self.addItem(item)

class ShowEntryWidget(QWebEngineView):
    """ Render the selected article's HTML

    Attributes:
    - entry_id (int)
    """
    def __init__(self, entry_raw):
        """
        Arguments:
        - entry_id(int) The id of the entry to render
        """
        super().__init__()
        self.entry_raw = entry_raw
        self.initUI()

    def initUI(self):
        entry = Entry(self.entry_raw)
        contents = entry.getContent()
        html_content = contents['content']
        self.setHtml(html_content)
        
        
