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
        self.itemDoubleClicked.connect(self.parent.categoryClicked)
        self.setFixedWidth(160)
        self.initUI()

    def initUI(self):
        categories = self.feedly.getCategories()
        for category in categories:
            item = QListWidgetItem(category.getLabel())
            item.setData(QtCore.Qt.UserRole, category)
            self.addItem(item)
