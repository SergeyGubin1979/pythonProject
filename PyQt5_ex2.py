import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QLabel, QHBoxLayout, QPushButton, QWidget)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        hbox = QHBoxLayout(self)
        pixmap = QPixmap("web.png")

        lbl = QLabel(self)
        lbl.setPixmap(pixmap)

        hbox.addWidget(lbl)

        btn = QPushButton('Buttom', self)
        btn.setToolTip('This is a <b>QWidjet</b> widget')
        btn.resize(70, 70)
        btn.move(50, 50)

        self.setLayout(hbox)

        self.move(300, 200)
        self.setWindowTitle('Ex2')
        self.show()

if __name__ =='__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit((app.exec_()))
    # commit
