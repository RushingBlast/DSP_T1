import sys
import pandas as pd

import threading
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QFileDialog,
)
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from viewerclass import signalViewer
from SignalViewer import SignalView
import pyedflib


class appwindow(QMainWindow):
    def __init__(self):
        super(appwindow, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.container = QWidget()
        signal_viewer_1 = SignalView()
        signal_viewer_2 = SignalView()
        signal_viewer_3 = SignalView()
        self.centralLayout = QtWidgets.QGridLayout()
        self.centralLayout.addWidget(signal_viewer_1)
        self.centralLayout.addWidget(signal_viewer_2)
        self.centralLayout.addWidget(signal_viewer_3)
        self.container.setLayout(self.centralLayout)
        appwindow.setCentralWidget(self,self.container)
        
 
app = QApplication(sys.argv)

window = appwindow()
window.show()
app.exec()
