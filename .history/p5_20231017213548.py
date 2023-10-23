from recycle import Ui_Form
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QGraphicsView, QDialog, QGridLayout, QShortcut
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import pyqtgraph as pg
import numpy as np
import sys
from pyqtgraph import PlotWidget, plot, PlotDataItem
from pathlib import Path



class class_signal_viewer(QWidget, Ui_Form):
    def __init__(self):
        super(class_signal_viewer, self).__init__()
        self.setupUi(self)
        self.btn_add_signal.setFocus()

################################################      CLASS VARIABLES      ################################################
        self.current_index= 0
        # self.selected_signal = pg.PlotDataItem()
        self.selected_signal = any
        self.max_range = 0
        self.last_reached_index = 0
        self.animation_running = False
        self.x = [[]]
        self.y = [[]]
        self.loaded_signals = []
        self.colors_list = ["r", "b","g","w","y","m"]
        # Set timer for update function
        self.timer = QtCore.QTimer(self)
        self.timer.stop()
        self.timer.timeout.connect(self.update)
        # self.animation_speed = 100  # Default speed
        

        
################################################      VIEW DETAILS      ################################################        

        self.view_widget.setLabel('bottom', 'Time')
        self.view_widget.setLabel('left', 'Amplitude')
        self.view_widget.setXRange(0,11,0)
        self.view_widget.setYRange(0,11,0)
        self.view_widget.setMouseEnabled(x=False, y=False)
        self.btn_zoom_in.setEnabled(False)
        self.btn_zoom_out.setEnabled(False)

################################################      BUTTONS CONNECTIONS      ################################################        

# ADD_SIGNAL_BTN        
        self.btn_add_signal.clicked.connect(self.add_signal)


# ZOOM_IN_BTN       
        self.btn_zoom_in.clicked.connect(self.zoom_in)


# ZOOM_OUT_BTN
        self.btn_zoom_out.clicked.connect(self.zoom_out)

# CLEAR_BTN
        self.btn_clear.clicked.connect(self.clear_signals)

# PLAY/PAUSE_BTN
        self.btn_start_pause.clicked.connect(self.toggle_animation)

# REMOVE_BTN
        self.btn_remove.clicked.connect(self.remove_selected_signal)



################################################      CLASS FUNCTIONS      ################################################


# Read csv files and save them in a list
    def read_signal_file(self):
        file_dialog = QFileDialog()
        file_dialog.exec()
        filename = file_dialog.selectedFiles().pop()
        path = str(Path(filename))
        pandas_data = pd.read_csv(path).iloc[:, 0]
        data = pandas_data.to_numpy()
        return data
    

# Return Clicked signal
    def return_clicked_signal(self):
        self.selected_signal = self.sender()
        
        signal_name = self.selected_signal.opts["name"]
        print(f"selected {signal_name}")
        for signal in self.loaded_signals:
            if signal is not self.sender():
                signal.setPen(signal.color, width= 0)
            else:
                signal.setPen(signal.color, width= 5)

# Remove Signal from Plot
    def remove_selected_signal(self):
        self.view_widget.removeItem(self.selected_signal)
        print(len(self.loaded_signals))
        # self.loaded_signals.remove(removed_signal)


# Update plot widget
    def update(self):
        if self.loaded_signals:
            for curve in self.loaded_signals:
                # curve= plotSignalItem()
                curve.setData(curve.original_data[0: self.current_index])        
            self.current_index+=1
                
    def move_signal(self, target_widget):
        if self.selected_signal:
            target_widget.view_widget.addLegend()
            self.selected_signal.setPen(self.selected_signal.color, width = 0)
            sent_signal = pg.PlotDataItem(x = self.selected_signal.getData()[0],y= self.selected_signal.getData()[1] , pen = self.selected_signal.opts['pen'], name = self.selected_signal.opts['name'] )
            target_widget.loaded_signals.append(sent_signal)
            self.view_widget.removeItem(self.selected_signal)
            target_widget.view_widget.addItem(sent_signal)
            target_widget.view_widget.autoRange()
            target_widget.loaded_signals.remove(self.selected_signal)
            self.selected_signal = None

# Add signals
    def add_signal(self):
        self.view_widget.addLegend()
        curve_color = random.choice(self.colors_list)
        
        data = self.read_signal_file()
        signal = pg.PlotDataItem(data, pen = curve_color, name = curve_color +"_Signal",clickable=True)
        signal.color = curve_color
        # Initialize loaded signal
        signal.original_data = data
        self.loaded_signals.append(signal)
        self.view_widget.addItem(signal)
        signal.sigClicked.connect(self.return_clicked_signal)
        
        self.view_widget.autoRange()

        # Enable plot widget mouse controls
        self.view_widget.setMouseEnabled(x=True, y=True)
        self.btn_zoom_in.setEnabled(True)
        self.btn_zoom_out.setEnabled(True)
        self.view_widget.setLimits(xMin=0, xMax=10000)
        self.horizontalScrollBar.valueChanged.connect(lambda value: self.view_widget.setXRange(value, value + 10))
        self.verticalScrollBar.valueChanged.connect(lambda value: self.view_widget.setYRange(value, value + 10))        

    def start_animation(self):
        # Calculate the animation interval based on the speed
        # interval = int(1000 / self.animation_speed)# Convert the interval to an integer
        self.timer.start(1)
        self.animation_running = True
        self.btn_start_pause.setChecked(False)
        self.btn_start_pause.setText('Stop Animation')
    
    def stop_animation(self):
        self.timer.stop()
        self.animation_running = False
        self.btn_start_pause.setChecked(True)
        self.btn_start_pause.setText('Play Animation')

    def toggle_animation(self):
        if self.animation_running:
            self.stop_animation()
        else:
            self.start_animation()



# Zoom in 
    def zoom_in(self):
        #Zoom in by adjusting x-axis limits (decrease window size)
        x_min, x_max = self.view_widget.viewRange()[0]
        window_size = x_max - x_min
        new_window_size = max(10, window_size * 0.88)  # Limit minimum window size
        center = (x_min + x_max) / 2
        self.view_widget.setXRange(center - new_window_size / 2, center + new_window_size / 2)
        

# Zoom out 
    def zoom_out(self):
        # Zoom out by adjusting x-axis limits (increase window size)
        x_min, x_max = self.view_widget.viewRange()[0]
        window_size = x_max - x_min
        new_window_size = window_size * 1.12  # Increase window size by 10%
        center = (x_min + x_max) / 2
        self.view_widget.setXRange(center - new_window_size / 2, center + new_window_size / 2, padding=0)

# # Move signal
#     def move_signals(self):
#         if self.view_widget is not None:     
#             self.view_widget.addLegend()
#             data = self.loaded_signals[len(self.loaded_signals)-1]
#             self.loaded_signals.append(data)
#             # print(len(self.loaded_signals))
#             # print(self.loaded_signals)
#             curve_color = random.choice(self.colors_list)
#             self.view_widget.plot(data, pen = curve_color, name = "Signal_" + str(len(self.loaded_signals)))
#             self.show()        

# Clear signals
    def clear_signals(self):
        self.view_widget.clear()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
