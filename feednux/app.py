import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QHBoxLayout, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

from ui.LeftMenu import LeftMenu
from ui.RightWidget import ShowStreamWidget
from ui.RightWidget import ShowEntryWidget

from feedly.Feedly import Feedly
from config import access_token

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "Feednux"
        self.initUI()

    def initUI(self):
        cw = CentralWidget()
        self.setCentralWidget(cw)
        self.setWindowTitle(self.title)
        self.show()


class CentralWidget(QWidget):
    """This is the central widget for the main class App. It takes no
    arguments to construct and is the widget on which other widgets
    are attached.

    """

    def __init__(self):
        super().__init__()
        self.feedly = Feedly(access_token)
        self.left = 0
        self.right = 0
        self.top = 10
        self.width = 320
        self.height = 240
        self.setStyleSheet("""
        QWidget {background-color: #e8eaef}
        """)
        self.initUI()

    def initUI(self):
        """Build the UI for the central widget. Takes no arguments."""
        
        self.hbox = QHBoxLayout(self)
        self.hbox.setSpacing(0)
        self.hbox.setAlignment(QtCore.Qt.AlignLeft)

        """:[Category] categories:"""
        categories = self.feedly.getCategories()
        
        """:LeftMenu(QListWidget): left_menu"""
        self.left_menu = LeftMenu(self)

        """:ShowStreamWidget(QListWidget): show_stream_widget"""
        self.right_widget = ShowStreamWidget(self, self.feedly, categories[0].getId())
        
        self.hbox.addWidget(self.left_menu)
        self.hbox.addWidget(self.right_widget)

        self.show()

    def _removeWidget(self, widget):
        self.hbox.removeWidget(widget)
        widget.close()
        widget = None

    def entryClicked(self, item):
        """Remove show_stream_widget and add show_entry_widget"""
        self._removeWidget(self.right_widget)

        chosen_entry = item.data(QtCore.Qt.UserRole)
        self.right_widget = ShowEntryWidget(chosen_entry.getRaw())
        self.hbox.addWidget(self.right_widget)
        
    def categoryClicked(self, item):
        self._removeWidget(self.right_widget)
        
        chosen_category = item.data(QtCore.Qt.UserRole)
        self.right_widget = ShowStreamWidget(self, self.feedly, chosen_category.getId())
        self.hbox.addWidget(self.right_widget)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
