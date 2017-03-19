from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5 import QtCore
from config import access_token

from feedly.Feedly import Feedly

class LeftMenu(QListWidget):
    """Render the menu on the left
    Attributes:
    - feedly (Feedly)
    """
    def __init__(self, parent):
        super().__init__()
        self.feedly = Feedly(access_token)
        self.parent = parent
        self.itemPressed.connect(self.parent.categoryClicked)
        self.setFixedWidth(250)
        self.setStyleSheet("""
        QListWidget {background-color: #3e4860; color: white}
        """)
        self.initUI()

    def initUI(self):
        categories = self.feedly.getCategories()
        for category in categories:
            item = QListWidgetItem(category.getLabel())
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setSizeHint(QtCore.QSize(250, 30))
            item.setData(QtCore.Qt.UserRole, category)
            self.addItem(item)
