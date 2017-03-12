from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5 import QtCore
from config import access_token

from feedly.Feedly import Feedly

class LeftMenu(QListWidget):
    """Render the menu on the left
    Attributes:
    - feedly (Feedly)
    """
    
    def __init__(self):
        super().__init__()
        self.feedly = Feedly(access_token)
        self.itemDoubleClicked.connect(self.itemClick)
        self.setFixedWidth(160)
        self.initUI()

    def initUI(self):
        categories = self.feedly.getCategories()
        for category in categories:
            item = QListWidgetItem(category.getLabel())
            item.setData(QtCore.Qt.UserRole, category)
            self.addItem(item)

    def itemClick(self, item):
        category = item.data(QtCore.Qt.UserRole)
        print(category.getLabel())
