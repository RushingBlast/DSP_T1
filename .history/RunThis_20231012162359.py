from new import Ui_MainWindow
import pandas as pd
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys
from itertools import count
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import pyedflib
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QGraphicsView, QDialog, QGridLayout
import numpy as np

################################################      GLOBAL CONSTANTS      ################################################

NUMBER_OF_DATAPOINTS = 10000 # Can be adjusted as needed
fixed_window_size = 300 # Ser the initla fixed window size





class myWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(myWindow, self).__init__()
        self.setupUi(self)
        
        self.x = [[]] #type:ignore
        self.y = [[]] #type:ignore
        
    # CLASS  VARIABLES
        
        self.loaded_signals = [] # List that holds currently loaded signals
        self.current_index = 0 # TODO Make a comment for this variable
        
        # X Min and Max for setting Xaxis range
        self.x_min_v1 = self.x_min_v2 = 0
        self.x_max_v1 = self.x_max_v2  = fixed_window_size
        self.counter = count(0,1)
        
        # Timers to drive animated playback for each view
        self.timer_v1 = self.timer_v2 = QtCore.QTimer(self)
        self.timer_v1.timeout.connect(self.update_v1)
        # self.timer_v2.timeout.connect(self.update_v2)
        # self.animation_running = False
        self.animation_running_v1 = False # Flag to track animation state
        self.animation_running_v2 = False # Flag to track animation state
        

        # Connect to buttons
        self.v1_widget.setLabel('bottom', 'Time')
        self.v1_widget.setLabel('left', 'Amplitude')
        self.v2_widget.setLabel('bottom', 'Time')
        self.v2_widget.setLabel('left', 'Amplitude')

        # self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.update_graph)
        # self.timer.start(50)  # Update every 50 milliseconds (adjust as desired)

# FILEMENU_OPEN_FILE
        self.actionOpen_File.triggered.connect(self.read_signal_file)

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

# PLAY_PAUSE_KEY
        self.v1_btn_start_pause.clicked.connect(self.toggle_animation_v1)
        self.v2_btn_start_pause.clicked.connect(self.toggle_animation_v2)
    
################################################      COMMON FUNCTIONS      ################################################


# Load Data from file and append them to signal list
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
                    
            else:
                # Unsupported file format
                error_UnsupportedFormat_msg = QtWidgets.QErrorMessage()
                error_UnsupportedFormat_msg.showMessage(f'Unsupported file format')
                
            
            
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

        # self.start_animation()
        
        
                    
                        
                    
            


                        
                                              

        
        
     


################################################      VIEW_1 FUNCTIONS      ################################################

# Add signals to view 1
    def v1_add_signal(self):
        if self.v1_widget is not None:
            self.v1_widget.clear()
        self.v1_widget.plot(self.read_signal_file())
        self.show()
        self.start_animation_v1()
        self.v1_btn_start_pause.setText('Stop Animation')
        self.v1_btn_start_pause.setChecked(True)
        

    
# Optimized version of Update_v1 
    def update_v1(self):
        loaded_signals_length = len(self.loaded_signals[0])
        if self.loaded_signals and self.current_index < loaded_signals_length:
            for loaded_signal, y_values, x_values in zip(self.loaded_signals, self.y, self.x): #type: ignore
                y_values.append(loaded_signal[self.current_index])
                x_values.append(self.current_index)

            self.v1_widget.clear()
            for x_values, y_values in zip(self.x, self.y): #type: ignore
                self.v1_widget.plot(x_values, y_values)
                if self.current_index >= self.x_max_v1:
                    self.x_min_v1 += 1
                    self.x_max_v1 += 1

            self.v1_widget.setXRange(self.x_min_v1, self.x_max_v1, padding=0)
            self.current_index += 1
        else:
            self.stop_animation_v1()
            
            
# Start signal playback for View 1
    def start_animation_v1(self):
        self.timer_v1.start(50)
        self.animation_running_v1 = True
        senderBtn = self.sender() # Returns object that sent the signal
        # if senderBtn is self.v1_btn_start_pause:
        #     senderBtn.
        if senderBtn is self.v1_btn_start_pause:
            senderBtn.setChecked(False) #type: ignore
            senderBtn.setText('Stop Animation') #type: ignore


# Stop Signal Playback for View 1
    def stop_animation_v1(self):
        self.timer_v1.stop()
        self.animation_running_v1 = False
        senderBtn = self.sender()
        if senderBtn is self.v1_btn_start_pause:
            senderBtn.setChecked(True) #type: ignore
            senderBtn.setText('Play Animation') #type: ignore

# Toggle signal playback for View 1
    def toggle_animation_v1(self):
        if self.animation_running_v1:
            self.stop_animation_v1()
        else:
            self.start_animation_v1()


# Zoom in view 1
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
        self.start_animation_v2()
        self.v2_btn_start_pause.setText('Stop Animation')
        self.v2_btn_start_pause.setChecked(True)
        
# Update View 2
    def update_v2(self):
        loaded_signals_length = len(self.loaded_signals[0])
        if self.loaded_signals and self.current_index < loaded_signals_length:
            for loaded_signal, y_values, x_values in zip(self.loaded_signals, self.y, self.x): #type: ignore
                y_values.append(loaded_signal[self.current_index])
                x_values.append(self.current_index)

            self.v2_widget.clear()
            for x_values, y_values in zip(self.x, self.y): #type: ignore
                self.v2_widget.plot(x_values, y_values)
                if self.current_index >= self.x_max_v2:
                    self.x_min_v2 += 1
                    self.x_max_v2 += 1

            self.v2_widget.setXRange(self.x_min_v2, self.x_max_v2, padding=0)
            self.current_index += 1
        else:
            self.stop_animation()
            
            
            
# Start signal playback for View 2
    def start_animation_v2(self):
        self.timer_v2.start(50)
        self.animation_running_v2 = True
        senderBtn = self.sender() # Returns object that sent the signal
        if senderBtn is self.v2_btn_start_pause:
            senderBtn.setChecked(False) #type: ignore
            senderBtn.setText('Stop Animation') #type: ignore



# Stop Signal Playback for View 2
    def stop_animation_v2(self):
        self.timer_v2.stop()
        self.animation_running_v2 = False
        senderBtn = self.sender()
        if senderBtn is self.v2_btn_start_pause:
            senderBtn.setChecked(True) #type: ignore
            senderBtn.setText('Play Animation') #type: ignore

# Toggle signal playback for View 2
    def toggle_animation_v2(self):
        if self.animation_running_v2:
            self.stop_animation_v2()
        else:
            self.start_animation_v2()
            
            
            
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






