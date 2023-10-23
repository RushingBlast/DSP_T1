from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QGraphicsView, QDialog, QGridLayout, QShortcut
from PyQt5 import QtCore, QtGui, QtWidgets
from p5 import class_signal_viewer
import sys

class main_window(QMainWindow):
    def __init__(self):
        super(main_window, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.container = QWidget()
        self.layout = QtWidgets.QHBoxLayout()
        signal_view_1 = class_signal_viewer()
        signal_view_2 = class_signal_viewer()
        self.layout.addWidget(signal_view_1)
        self.layout.addWidget(signal_view_2)
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)
        signal_view_1.setFocus()
        self.setMinimumSize(700, 500)

        # Setting up signal tranfer by linking views
        signal_view_1.btn_clone_signal2.clicked.connect(lambda: signal_view_1.move_signal(signal_view_2))
        signal_view_2.btn_clone_signal2.clicked.connect(lambda: signal_view_2.move_signal(signal_view_1))
        signal_1_loaded_signals = signal_view_1.get_loaded_signals
        signal_2_loaded_signals = signal_view_2.get_loaded_signals






app = QApplication(sys.argv)
win = main_window()
win.show()
app.exec()
