from PyQt5.QtWidgets import (
    QPushButton,
    QTextEdit,
    QDialog,
    QFileDialog,
    QListWidget,
    QListWidgetItem,
    QListView,
    QVBoxLayout,
    QHBoxLayout
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
        QListWidget {background-color: #3e4860;
        color: #D0D4E0; font: 12px; width:100%}
        """)
        self.initUI()

    def initUI(self):
        self.itemClicked.connect(self.itemClick)

        importButton = QListWidgetItem("Import OPML")
        importButton.setData(QtCore.Qt.UserRole, importButton)
        self.addItem(importButton)

        addFeedButton = QListWidgetItem("Add New Feed")
        addFeedButton.setData(QtCore.Qt.UserRole, addFeedButton)
        self.addItem(addFeedButton)

        self.show()

    def itemClick(self, item):
        itemName = item.text()

        if itemName == "Import OPML":
            self.importOPML()
        elif itemName == "Add New Feed":
            self.addNewFeed()

    def importOPML(self):
        fd = QFileDialog(self)
        filename = fd.getOpenFileName()
        l = Local()
        l.parseOpml(filename[0])

    def addNewFeed(self):
        nf = NewFeedDialog(self)
        nf.show()


class NewFeedDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet("""
        QDialog::QTextEdit{width: 90%; height: 16px}
        """)
        self.urlInput = QTextEdit(self)
        self.acceptButton = QPushButton("Add")
        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.clicked.connect(self.closeDialog)
        self.acceptButton.clicked.connect(self.addURL)
        self.initUI()

    def initUI(self):
        self.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))

        self.vbox = QVBoxLayout(self)
        self.vbox.setSpacing(0)
        self.vbox.setAlignment(QtCore.Qt.AlignTop)

        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(0)
        self.vbox.setAlignment(QtCore.Qt.AlignLeft)

        self.label = QTextEdit("Add url:")
        self.label.setReadOnly(True)
        self.label.setMaximumHeight(30)
        self.vbox.addWidget(self.label)

        self.urlInput.setMaximumHeight(30)
        self.vbox.addWidget(self.urlInput)

        self.hbox.addWidget(self.acceptButton)
        self.hbox.addWidget(self.cancelButton)

        self.vbox.addLayout(self.hbox)

    def closeDialog(self):
        self.close()

    def addURL(self):
        url = self.urlInput.toPlainText()
        l = Local()
        l.addFeed(url)
        self.close()
