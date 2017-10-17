import sys
from PyQt5.QtWidgets import (
    QFileDialog,
    QApplication,
    QWidget,
    QMainWindow,
    QHBoxLayout,
)
from PyQt5 import QtCore

from ui.LeftMenu import LeftMenu
from ui.RightWidget import ShowStreamWidget
from ui.RightWidget import ShowEntryWidget
from ui.MenuBar import MenuBar

from local.Local import Local


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = "Feednux"
        self.frameSize()
        self.initUI()

    def initUI(self):
        cw = CentralWidget()
        mb = MenuBar()
        self.setMenuWidget(mb)
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
        self.local = Local()
        self.setStyleSheet("""
        QWidget {background-color: #e8eaef; border: 0px}
        """)
        self.initUI()

    def initUI(self):
        self.setContentsMargins(QtCore.QMargins(0, 0, 0, 0))
        """Build the UI for the central widget. Takes no arguments."""
        self.hbox = QHBoxLayout(self)
        self.hbox.setSpacing(0)
        self.hbox.setAlignment(QtCore.Qt.AlignLeft)

        feeds = self.local.getFeeds()

        if len(feeds) == 0:
            filename = self._openFileDialog()

            if filename[0] == "":
                self.parent().close()
            self.local.parseOpml(filename[0])
            feeds = self.local.getFeeds()

        """:LeftMenu(QListWidget): left_menu"""
        self.left_menu = LeftMenu(self)

        """:ShowStreamWidget(QListWidget): show_stream_widget"""
        self.right_widget = ShowStreamWidget(self, self.local,
                                                     feeds[0])

        self.hbox.addWidget(self.left_menu)
        self.hbox.addWidget(self.right_widget)

        self.show()

    def _openFileDialog(self):
            fd = QFileDialog(self, "Import OPML file")
            filename = fd.getOpenFileName()
            return filename


    def _removeWidget(self, widget):
        self.hbox.removeWidget(widget)
        widget.close()
        widget = None

    def entryClicked(self, item):
        """Remove show_stream_widget and add show_entry_widget"""
        self._removeWidget(self.right_widget)

        chosen_entry = item.data(QtCore.Qt.UserRole)
        self.right_widget = ShowEntryWidget(chosen_entry)
        self.hbox.addWidget(self.right_widget)

    def categoryClicked(self, item):
        self._removeWidget(self.right_widget)

        chosen_feed = item.data(QtCore.Qt.UserRole)
        self.right_widget = ShowStreamWidget(self, self.local,
                                             chosen_feed)
        self.hbox.addWidget(self.right_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
