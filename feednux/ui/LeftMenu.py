from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5 import QtCore

from local.Local import Local


class LeftMenu(QListWidget):
    """Render the menu on the left
    Attributes:
    - feedly (Feedly)
    """
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.local = Local()
        self.itemPressed.connect(self.parent.categoryClicked)
        self.setFixedWidth(250)
        self.setStyleSheet("""
        QListWidget {background-color: #3e4860; color: white}
        QListWidget::item:hover:!pressed {background-color: #6c7a9b}
        QListWidget::item:selected {background-color: #6c7a9b}
        """)
        self.initUI()

    def initUI(self):
        feeds = self.local.getFeeds()
        for feed in feeds:
            item = QListWidgetItem(feed[1])
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setSizeHint(QtCore.QSize(250, 30))
            item.setData(QtCore.Qt.UserRole, feed)
            self.addItem(item)
