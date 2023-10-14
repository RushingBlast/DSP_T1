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
        global signal_viewer_1, signal_viewer_2, signal_viewer_3
        
 
        
        
        self.linking_enabled = False
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
        
        signal_viewer_1.btn_play_pause.clicked.connect(self.toggle_linking)
        
        signal_viewer_1.graphicsView.setLimits(xMin = 0, xMax = 10000, yMin = 0, yMax = 100000)
        signal_viewer_2.graphicsView.setLimits(xMin = 0, xMax = 10000, yMin = 0, yMax = 100000)
        
        
        # Generate some example data
        x = [0, 1, 2, 3, 4, 5]
        y = [0, 1, 4, 9, 16, 25]

        # Create the plot items and add them to the plot widgets
        plot_item1 = signal_viewer_1.graphicsView.plot(x, y, pen='r')
        plot_item2 = signal_viewer_2.graphicsView.plot(x, y, pen='b')
        signal_viewer_1.graphicsView.sigXRangeChanged.connect(self.update_plot1_x_range)
        signal_viewer_2.graphicsView.sigXRangeChanged.connect(self.update_plot2_x_range)
        signal_viewer_1.graphicsView.sigYRangeChanged.connect(self.update_plot1_y_range)
        signal_viewer_2.graphicsView.sigYRangeChanged.connect(self.update_plot2_y_range)
        

    def toggle_linking(self):
        self.linking_enabled = not self.linking_enabled
        self.update_plot2_x_range()
        self.update_plot1_x_range()
        self.update_plot1_y_range()
        self.update_plot2_y_range()
        
        QApplication.processEvents()
        
        
    def update_plot1_x_range(self):
        if self.linking_enabled:
            signal_viewer_2.graphicsView.setXRange(*signal_viewer_1.graphicsView.viewRange()[0], padding = 0)
    
    def update_plot2_x_range(self):
        if self.linking_enabled:    
            signal_viewer_1.graphicsView.setXRange(*signal_viewer_2.graphicsView.viewRange()[0], padding = 0)

    def update_plot1_y_range(self):
        if self.linking_enabled:    
            signal_viewer_2.graphicsView.setYRange(*signal_viewer_1.graphicsView.viewRange()[1], padding = 0)
    
    def update_plot2_y_range(self):
        if self.linking_enabled:    
            signal_viewer_1.graphicsView.setYRange(*signal_viewer_2.graphicsView.viewRange()[1], padding = 0)
        
app = QApplication(sys.argv)

window = appwindow()
window.show()
app.exec()
