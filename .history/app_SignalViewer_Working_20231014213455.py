import sys
import numpy as np
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QPushButton,
    QFileDialog,
    QAction,
    QMenu
)
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from ui_mainInterface import Ui_mainWindow_SignalViewer
from class_SignalViewer_noPlotDataItem import SignalView


class appwindow(QMainWindow, Ui_mainWindow_SignalViewer):
    def __init__(self):
        super(appwindow, self).__init__()
####### Initialize Ui
        self.initUI()
      
####### Application variables
        # Flag to govern linking the signalViewers
        self.linking_enabled = False  
        
        # Flag to unlink views during animation playback
        self.link_x_range_of_views = False
####### Connecting Signals of UI elements
        # Toggle Linking the signal viewers when selecting "Link" from file menu
        self.linkAction.triggered.connect(self.toggle_linking)
        
        
        

####### Method to setup the UI
    def initUI(self):
        
        self.setupUi(self)
        
    # SETTING UP THE UI
        global signal_viewer_1, signal_viewer_2
        
        # Creating and setting menu bar
        menuBar = self.menuBar()
        self.setMenuBar(menuBar)
        
        # Creating the File menu
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        
        
        # Creating and adding Action to File Menu
        self.linkAction = QAction("&Link", self)
        fileMenu.addAction(self.linkAction)
        
        
        
        
        # Setting up the main window
        signal_viewer_1 = SignalView()
        signal_viewer_1.setFocusPolicy(QtCore.Qt.StrongFocus)
        signal_viewer_2 = SignalView()
        self.centralLayout = QtWidgets.QGridLayout()
        self.grid_signal_viewers.addWidget(signal_viewer_1)
        self.grid_signal_viewers.addWidget(signal_viewer_2)
        # self.centralLayout.addWidget(signal_viewer_1)
        # self.centralLayout.addWidget(signal_viewer_2)
        # self.container.setLayout(self.centralLayout)
        # appwindow.setCentralWidget(self,self.container)
        
        
        # Prevent signal viewers from going past X=0 and Y=0      
        signal_viewer_1.plot_widget.setLimits(xMin = 0, yMin = -5)
        signal_viewer_2.plot_widget.setLimits(xMin = 0, yMin = -5)
        
        

        signal_viewer_1.plot_widget.sigXRangeChanged.connect(self.update_plot1_x_range)
        signal_viewer_2.plot_widget.sigXRangeChanged.connect(self.update_plot2_x_range)
        signal_viewer_1.plot_widget.sigYRangeChanged.connect(self.update_plot1_y_range)
        signal_viewer_2.plot_widget.sigYRangeChanged.connect(self.update_plot2_y_range)
        
    # Function the toggles Linking the views
    def toggle_linking(self):
        self.linking_enabled = not self.linking_enabled
        if self.linking_enabled:
            self.linkAction.setText("Unlink")
            signal_viewer_1.start_button.clicked.disconnect(signal_viewer_1.toggle_animation)
            signal_viewer_1.start_button.clicked.connect(self.linked_animation_playback)
            # signal_viewer_2.start_button.clicked.connect(self.linked_animation_playback)
            signal_viewer_2.button_container.setVisible(False)
            signal_viewer_2.button_container.setEnabled(False)
            
            # Reset both views to prepare for linked playback
            signal_viewer_1.clean_plot()
            signal_viewer_2.clean_plot()
            signal_viewer_1.toggle_animation()
            signal_viewer_2.toggle_animation()
            
            minimum_x_max = np.minimum(signal_viewer_1.x_max, signal_viewer_2.x_max)
            signal_viewer_1.x_min = signal_viewer_2.x_min
            signal_viewer_1.x_max = signal_viewer_2.x_max = minimum_x_max
            signal_viewer_1.plot_widget.autoRange()
            
            
        else:
            self.linkAction.setText("Link")
            signal_viewer_1.start_button.clicked.disconnect(self.linked_animation_playback)
            signal_viewer_1.start_button.clicked.connect(signal_viewer_1.toggle_animation)
            signal_viewer_2.button_container.setVisible(True)
            signal_viewer_2.button_container.setEnabled(True)
            
        self.update_plot1_x_range()
        self.update_plot2_x_range()
        self.update_plot1_y_range()
        self.update_plot2_y_range()
        QApplication.processEvents()
    
    def linked_animation_playback(self):
        if self.link_x_range_of_views:
            signal_viewer_1.plot_widget.sigXRangeChanged.connect(self.update_plot1_x_range)
            signal_viewer_2.plot_widget.sigXRangeChanged.connect(self.update_plot2_x_range)
        else:
            
            signal_viewer_1.plot_widget.sigXRangeChanged.disconnect(self.update_plot1_x_range)
            signal_viewer_2.plot_widget.sigXRangeChanged.disconnect(self.update_plot2_x_range)
        signal_viewer_1.toggle_animation()
        signal_viewer_2.toggle_animation()
        
    def update_plot1_x_range(self):
        if self.linking_enabled:
            signal_viewer_2.plot_widget.setXRange(*signal_viewer_1.plot_widget.viewRange()[0], padding = 0)
    
    def update_plot2_x_range(self):
        if self.linking_enabled:    
            signal_viewer_1.plot_widget.setXRange(*signal_viewer_2.plot_widget.viewRange()[0], padding = 0)

    def update_plot1_y_range(self):
        if self.linking_enabled:    
            signal_viewer_2.plot_widget.setYRange(*signal_viewer_1.plot_widget.viewRange()[1], padding = 0)
    
    def update_plot2_y_range(self):
        if self.linking_enabled:    
            signal_viewer_1.plot_widget.setYRange(*signal_viewer_2.plot_widget.viewRange()[1], padding = 0)
        
app = QApplication(sys.argv)

window = appwindow()
window.show()
app.exec()
