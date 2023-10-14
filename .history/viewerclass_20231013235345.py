import sys
import pandas as pd
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QFileDialog
from viewerUI import Ui_viewer 
import pyedflib

class signalViewer(QWidget, Ui_viewer):
    def __init__(self):
        super(signalViewer, self).__init__()
        self.setupUi(self)
        
        placeholder_plot = pg.plot(title = "placeholder_plot")
        # self.graphicsView.addItem(placeholder_plot)
        placeholder_plot.show()
        
        self.btn_play_pause.clicked.connect(lambda: print("Play/Pause Clicked!"))
        self.btn_openfile.clicked.connect(lambda: print("Open File Clicked!"))
        
        
# app = QApplication(sys.argv)
# signalV = signalViewer()
# signalV.show()
# app.exec()