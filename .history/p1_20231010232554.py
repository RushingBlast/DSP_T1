import pandas as pd
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys
from pathlib import Path
import matplotlib
from PyQt5 import QtCore, QtGui, QtWidgets  
from new import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QGraphicsView, QDialog, QGridLayout
import numpy as np

################################################      GLOBAL CONSTANTS      ################################################
number_of_datapoints = 1000





class myWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(myWindow, self).__init__()
        self.setupUi(self)
        self.x = [[]]
        self.y = [[]]
        self.loaded_signals = []
        # class variables
        

        # Connect to buttons
        self.v1_widget.setLabel('bottom', 'Time')
        self.v1_widget.setLabel('left', 'Amplitude')
        self.v2_widget.setLabel('bottom', 'Time')
        self.v2_widget.setLabel('left', 'Amplitude')

        # self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.update_graph)
        # self.timer.start(50)  # Update every 50 milliseconds (adjust as desired)


# ADD_SIGNAL_BTNs        
        self.v1_btn_add_signal.clicked.connect(self.v1_add_signal)
        self.v2_btn_add_signal.clicked.connect(self.v2_add_signal)

# ZOOM_IN_BTNs       
        self.v1_btn_zoom_in.clicked.connect(self.v1_zoom_in)
        self.v2_btn_zoom_in.clicked.connect(self.v2_zoom_in)

# ZOOM_OUT_BTNs
        self.v1_btn_zoom_out.clicked.connect(self.v1_zoom_out)
        self.v2_btn_zoom_out.clicked.connect(self.v2_zoom_out)

# MOVE_LEFT_BTNs
        self.v1_btn_move_left.clicked.connect(self.v1_move_left)
        self.v2_btn_move_left.clicked.connect(self.v2_move_left)

# MOVE_RIGHT_BTNs
        self.v1_btn_move_right.clicked.connect(self.v1_move_right)
        self.v2_btn_move_right.clicked.connect(self.v2_move_right)

    
################################################      COMMON FUNCTIONS      ################################################

# TODO Remove this early file opening function if new one works
"""
# Read csv files and save them in a list
    def read_signal_file(self):
        file_dialog = QFileDialog()
        file_dialog.exec()
        filename = file_dialog.selectedFiles().pop()
        path = str(Path(filename))
        data = pd.read_csv(path).iloc[:, 0]
        # save signals
        # self.loaded_signals.append(data.iloc[:, 0].tolist())
        # print(len(self.loaded_signals))
        return data
"""    
    def read_signal_file(self):

        # Open a file dialog to select a file with supported extensions
        open_file_dialog = QFileDialog.Options()
        open_file_dialog |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Data File", "", "CSV Files (*.csv);;EDF Files (*.edf);; DAT Files (*.dat)", options = open_file_dialog
        )

        if file_path:
            file_extension = file_path.split('.')[-1]
            if file_extension.lower() == 'csv':
                #load the CSV File containing signal data
                datafile = pd.read_csv(file_path)
            elif file_extension.lower() == 'edf':
                 try:
                      # Load EDF file using pyedflib
                      edf_file_reader = pyedfilb.EdfReader(file_path)
                      num_signals = edf_file_reader.signals_in_file
                      signal_data = []
                      for i in range(num_signals):
                           signal_data.append(edf_file_reader.readSignal(i)[:N])
                                              

        
        
     


################################################      VIEW_1 FUNCTIONS      ################################################

# Add signals to view 1
    def v1_add_signal(self):
        if self.v1_widget is not None:
            self.v1_widget.clear()
        self.v1_widget.plot(self.read_signal_file())
        self.show()


#x Zoom in view 1
    def v1_zoom_in(self):
        # Zoom in by adjusting x-axis limits (decrease window size)
        x_min, x_max = self.v1_widget.viewRange()[0]
        window_size = x_max - x_min
        window_size = x_max - x_min
        new_window_size = max(10, window_size * 0.88)  # Limit minimum window size
        center = (x_min + x_max) / 2
        self.v1_widget.setXRange(center - new_window_size / 2, center + new_window_size / 2, padding=0)
        
# Zoom out view 1
    def v1_zoom_out(self):
        # Zoom out by adjusting x-axis limits (increase window size)
        x_min, x_max = self.v1_widget.viewRange()[0]
        window_size = x_max - x_min
        new_window_size = window_size * 1.12  # Increase window size by 10%
        center = (x_min + x_max) / 2
        self.v1_widget.setXRange(center - new_window_size / 2, center + new_window_size / 2, padding=0)

# Move left in view 1
    def v1_move_left(self):
            # Move the visible range left by 50 data points
            x_min, x_max = self.v1_widget.viewRange()[0]
            x_min -= 50
            x_max -= 50
            self.v1_widget.setXRange(x_min, x_max, padding=0)

# Move right in view 1
    def v1_move_right(self):
            # Move the visible range left by 50 data points
            x_min, x_max = self.v1_widget.viewRange()[0]
            x_min += 50
            x_max += 50
            self.v1_widget.setXRange(x_min, x_max, padding=0)


    


################################################      VIEW_2 FUNCTIONS      ################################################


# Add signals to view 2
    def v2_add_signal(self):
        if self.v2_widget is not None:
            self.v2_widget.clear()
        self.v2_widget.plot(self.read_signal_file())
        self.show()

# Zoom in view 2        
    def v2_zoom_in(self):
        # Zoom in by adjusting x-axis limits (decrease window size)
        x_min, x_max = self.v2_widget.viewRange()[0]
        window_size = x_max - x_min
        window_size = x_max - x_min
        new_window_size = max(10, window_size * 0.88)  # Limit minimum window size
        center = (x_min + x_max) / 2
        self.v2_widget.setXRange(center - new_window_size / 2, center + new_window_size / 2, padding=0)

# Zoom out view 2
    def v2_zoom_out(self):
        # Zoom out by adjusting x-axis limits (increase window size)
        x_min, x_max = self.v2_widget.viewRange()[0]
        window_size = x_max - x_min
        new_window_size = window_size * 1.12  # Increase window size by 10%
        center = (x_min + x_max) / 2
        self.v2_widget.setXRange(center - new_window_size / 2, center + new_window_size / 2, padding=0)


# Move left in view 2
    def v2_move_left(self):
            # Move the visible range left by 50 data points
            x_min, x_max = self.v2_widget.viewRange()[0]
            x_min -= 50
            x_max -= 50
            self.v2_widget.setXRange(x_min, x_max, padding=0)
   
# Move right in view 2
    def v2_move_right(self):
            # Move the visible range left by 50 data points
            x_min, x_max = self.v2_widget.viewRange()[0]
            x_min += 50
            x_max += 50
            self.v2_widget.setXRange(x_min, x_max, padding=0)
    
##############################################################################################################################
app = QApplication(sys.argv)

#Create the main window and make it shown
homewindow = myWindow()
homewindow.show()

# Execute application
app.exec()






