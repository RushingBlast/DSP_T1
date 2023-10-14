import sys
import pandas as pd

import threading
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QFileDialog
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from viewerclass import signalViewer
# from SignalViewer import SignalView
import pyedflib


class appwindow(QMainWindow):
    def __init__(self):
        super(appwindow, self).__init__()
        self.initUI()
        
        
    def initUI(self):
        self.container = QWidget()
        signal_viewer_1 = signalViewer()
        signal_viewer_2 = signalViewer()
        signal_viewer_3 = signalViewer()
        self.centralLayout = QtWidgets.QGridLayout()
        self.centralLayout.addWidget(signal_viewer_1)
        self.centralLayout.addWidget(signal_viewer_2)
        self.centralLayout.addWidget(signal_viewer_3)
        self.container.setLayout(self.centralLayout)
        appwindow.setCentralWidget(self,self.container)
        
        # Generate some example data
        x = [0, 1, 2, 3, 4, 5]
        y = [0, 1, 4, 9, 16, 25]

        # Create the plot items and add them to the plot widgets
        plot_item1 = signal_viewer_1.graphicsView.plot(x, y, pen='r')
        plot_item2 = signal_viewer_2.graphicsView.plot(x, y, pen='b')
        signal_viewer_1.graphicsView.set
        # thread_1 = threading.Thread(target=signal_viewer_1.run_in_thread)
        # thread_2 = threading.Thread(target=signal_viewer_2.run_in_thread)
        # thread_3 = threading.Thread(target=signal_viewer_3.run_in_thread)

        # thread_1.start()
        # thread_2.start()
        # thread_3.start()
    def update_plot1_range():
        signal_viewer_2.graphicsView.set
app = QApplication(sys.argv)

window = appwindow()
window.show()
app.exec()
