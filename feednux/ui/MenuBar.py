from PyQt5.QtWidgets import (
    QFileDialog,
    QListWidget,
    QListWidgetItem,
    QListView
)
from PyQt5 import QtCore
from local.Local import Local


class MenuBar(QListWidget):

    def __init__(self):
        super().__init__()
        flow = QListView.LeftToRight
        self.setFlow(flow)
        self.setMaximumHeight(18)
        self.setStyleSheet("""
        QListWidget {background-color: #3e4860; color: #D0D4E0; font: 12px}
        """)
        self.initUI()

    def initUI(self):
        item = QListWidgetItem("Import OPML")
        item.setData(QtCore.Qt.UserRole, item)
        self.itemClicked.connect(self.itemClick)
        self.addItem(item)
        self.show()

    def itemClick(self, item):
        itemName = item.text()

        if itemName == "Import OPML":
            self.importOPML()

    def importOPML(self):
        fd = QFileDialog(self)
        filename = fd.getOpenFileName()
        l = Local()
        l.parseOpml(filename[0])
