from new import Ui_MainWindow
import pandas as pd
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import pyedflib
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QGraphicsView, QDialog, QGridLayout
import numpy as np

################################################      GLOBAL CONSTANTS      ################################################

NUMBER_OF_DATAPOINTS = 10000 # Can be adjusted as needed





class myWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(myWindow, self).__init__()
        self.setupUi(self)
        
        # uic.loadUi('p1.ui', self)
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
# """
# Read csv files and save them in a list
#     def read_signal_file(self):
#         file_dialog = QFileDialog()
#         file_dialog.exec()
#         filename = file_dialog.selectedFiles().pop()
#         path = str(Path(filename))
#         data = pd.read_csv(path).iloc[:, 0]
#         # save signals
#         # self.loaded_signals.append(data.iloc[:, 0].tolist())
#         # print(len(self.loaded_signals))
#         return data
# """    
    def read_signal_file(self,view):

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
                dataFrame = pd.read_csv(file_path)

            # Handling import of EDF file
            elif file_extension.lower() == 'edf':
                try:
                    # Load EDF file using pyedflib
                    edf_file_reader = pyedflib.EdfReader(file_path)
                    num_signals = edf_file_reader.signals_in_file
                    signal_data = []
                    for i in range(num_signals):
                        signal_data.append(edf_file_reader.readSignal(i)[:NUMBER_OF_DATAPOINTS])
                    edf_file_reader.close()
    
                    # Convert the EDF data to a DataFrame
                    dataFrame = pd.DataFrame(signal_data).T

                # Throw an Exception if loading EDF File failed
                except Exception as e:
                    error_LoadEDF_msg = QtWidgets.QErrorMessage()
                    error_LoadEDF_msg.showMessage(f'Error loading EDF file: {str(e)}')
                    return

            # Handling import of DAT file
            elif file_extension.lower() == 'dat' :
                try:
                    # Load DAT File as binary
                    with open(file_path, 'rb') as dat_file: # 'rb' is just an argument to open file in 'Read in Binary' mode
                        # Read the binary data
                        binary_data = dat_file.read()
                        
                        
                        # Assuming the data is a series of floars, you can unpack it like this
                        # Adjust the struct format string according to your data format
                        import struct 
                        data_format = 'f' * (len(binary_data) // struct.calcsize('f'))
                        dat_data = struct.unpack(data_format, binary_data)
                        
                        # Create a single-column DataFrame from DAT Data
                        dataFrame = pd.DataFrame(dat_data)
                        
                # Throw an Exception if loading DAT File failed
                except Exception as e:
                    error_LoadDAT_msg = QtWidgets.QErrorMessage()
                    error_LoadDAT_msg.showMessage(f'Error loading DAT file: {str(e)}')
                    return
            else:
                # Unsupported file format
                error_UnsupportedFormat_msg = QtWidgets.QErrorMessage()
                error_UnsupportedFormat_msg.showMessage(f'Unsupported file format')
                return
            
            
            # Extract the signal data and create a new PlotItem for it
            loaded_signal = dataFrame.iloc[:NUMBER_OF_DATAPOINTS, 0].tolist()
            self.loaded_signals.append(loaded_signal)
            self.x.append([])
            self.y.append([])
            
            return loaded_signal

            # plot_item = self.view.getPlotItem()
            # plot_item.setLabel('bottom', 'Time')
            # plot_item.setLabel('left', 'Amplitude')
            # plot_item.plot(pen='g')  # Create a new plot in the PlotItem

        self.start_animation()
                    
                        
                    
            


                        
                                              

        
        
     


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






