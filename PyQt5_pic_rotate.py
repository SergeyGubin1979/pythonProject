import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QLabel, QGridLayout,
                             QPushButton)
from PyQt5.QtGui import QPixmap

class myApplication(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(myApplication, self).__init__(parent)
        self.rotation = 0

        self.pixmap = QtGui.QPixmap("web.png")

        self.label = QLabel()
        self.label.setMaximumSize(400, 400)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setPixmap(self.pixmap)

        button = QPushButton("Rotate 15 degrees")
        button.clicked.connect(self.rotate_pixmap)

        grid = QGridLayout(self)
        grid.addWidget(self.label, 0, 0)
        grid.addWidget(button, 1, 0)

    def rotate_pixmap(self):
        pixmap = self.pixmap.copy()
        self.rotation +=15
        transform = QtGui.QTransform().rotate(self.rotation)
        pixmap = pixmap.transformed(transform, QtCore.Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)

if __name__ =='__main__':
    app = QApplication([])

    w = myApplication()
    w.show()

    sys.exit(app.exec_())

