import sys
import random
from PyQt5 import QtCore
import pandas as pd
import numpy as np
import pyqtgraph as pg
from itertools import count
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QGridLayout,
    QHBoxLayout,
    QFileDialog,
    QShortcut,
    QSlider  # Import QSlider for speed control
)
import pyedflib

# Just a Placeholder key for shortcuts
# placeholder_key = Qt.Key.Key_unknown

fixed_window_size = 300  # Set the initial fixed window size
# Initialize some variables
N = 10000  # Number of data points (adjust as needed)
t = np.linspace(0, 0, N)
ptr = -N
# y = np.zeros(N)
frame_times = np.zeros(N)  # Add this attribute to store frame times


class SignalView(QWidget):
    def __init__(self, play_pause_key = Qt.Key.Key_Space, move_left_key = Qt.Key.Key_Left, move_right_key = Qt.Key.Key_Right, load_csv_key = Qt.Key.Key_Control + Qt.Key.Key_O, zoom_in_key = Qt.Key.Key_Control + Qt.Key.Key_Up, zoom_out_key = Qt.Key.Key_Control + Qt.Key.Key_Down, parent=None):
        super().__init__(parent)

        self.x = [[]]
        self.y = [[]]
        self.current_index = 0
        self.x_min = 0
        self.x_max = fixed_window_size  # Initially set x_max to fixed_window_size
        self.loaded_signals = []  # List to store loaded signal data
        self.colors_list = ["Red", "Green", "Blue", "Yellow"]

        # Create shortcuts        
        self.play_pause_shortcut = QShortcut(play_pause_key, self)
        self.play_pause_shortcut.activated.connect(self.toggle_animation)

        self.move_left_shortcut = QShortcut(move_left_key, self)
        self.move_left_shortcut.activated.connect(self.move_left)

        self.move_right_shortcut = QShortcut(move_right_key, self)
        self.move_right_shortcut.activated.connect(self.move_right)

        self.open_file_shortcut = QShortcut(load_csv_key, self)
        self.open_file_shortcut.activated.connect(self.add_new_signal)

        self.zoom_in_shortcut = QShortcut(zoom_in_key, self)
        self.zoom_in_shortcut.activated.connect(self.zoom_in)

        self.zoom_out_shortcut = QShortcut(zoom_out_key, self)
        self.zoom_out_shortcut.activated.connect(self.zoom_out)

        self.initUI()

    def initUI(self):
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel('bottom', 'Time')
        self.plot_widget.setLabel('left', 'Amplitude')
        
        #Container that holds the buttons so it can be hid or shown
        self.button_container = QWidget()
        
        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        
        # Horizontal layout to carry the control buttons
        button_layout = QHBoxLayout()
        # Vertical layout to carry the slider and button layout
        button_slider_layout = QVBoxLayout()
        
        # Add Start Animation button
        self.start_button = QPushButton('Stop Animation')
        self.start_button.setCheckable(True)  # Make the button checkable (toggle)
        self.start_button.clicked.connect(self.toggle_animation)
        button_layout.addWidget(self.start_button)
        # Add button to move left
        self.left_button = QPushButton('Move Left')
        self.left_button.clicked.connect(self.move_left)
        button_layout.addWidget(self.left_button)
        # Add button to move right
        self.right_button = QPushButton('Move Right')
        self.right_button.clicked.connect(self.move_right)
        button_layout.addWidget(self.right_button)

        # Add a button to load a new CSV file
        self.load_button = QPushButton('Load CSV')
        self.load_button.clicked.connect(self.add_new_signal)
        button_layout.addWidget(self.load_button)
        # Add Zoom in button
        self.zoom_in_button = QPushButton('Zoom In')
        self.zoom_in_button.clicked.connect(self.zoom_in)
        button_layout.addWidget(self.zoom_in_button)
        # Add Zoom out button
        self.zoom_out_button = QPushButton('Zoom Out')
        self.zoom_out_button.clicked.connect(self.zoom_out)
        button_layout.addWidget(self.zoom_out_button)
        
        # Add a speed control slider
        self.speed_slider = QSlider(Qt.Horizontal)
        self.speed_slider.setMinimum(1)  # Minimum speed
        self.speed_slider.setMaximum(500)  # Maximum speed
        self.speed_slider.setValue(100)  # Initial speed
        self.speed_slider.setTickPosition(QSlider.TicksBelow)
        self.speed_slider.setTickInterval(10)
        self.speed_slider.valueChanged.connect(self.update_speed)
        
        
        button_slider_layout.addLayout(button_layout)
        button_slider_layout.addWidget(self.speed_slider)
        self.button_container.setLayout(button_slider_layout)



        layout.addWidget(self.button_container)


        self.setLayout(layout)

        self.counter = count(0, 1)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.animation_speed = 100  # Default speed
        self.start_animation()
        
    def update_speed(self):
            # Update the animation speed based on the slider value
            self.animation_speed = self.speed_slider.value()
            if self.animation_running:
                self.start_animation()  # Restart the animation with the updated speed

    
    def update(self):
        if self.loaded_signals and self.current_index < len(self.loaded_signals[0]):
            for i in range(len(self.loaded_signals)):
                self.y[i].append(self.loaded_signals[i][self.current_index])
                self.x[i].append(self.current_index)  # Use the index as a simple time placeholder

                # Adjust x-axis limits to create a scrolling effect
                if self.current_index >= self.x_max:
                    self.x_min += 1
                    self.x_max += 1

            self.plot_widget.clear()
            for i in range(len(self.loaded_signals)):
                self.plot_widget.plot(self.x[i], self.y[i])

            self.plot_widget.setXRange(self.x_min, self.x_max, padding=0)  # Set x-axis limits with no padding
            self.current_index += 1
            QApplication.processEvents()
        else:
            self.stop_animation()


    def zoom_in(self):
        # Zoom in by adjusting x-axis limits (decrease window size)
        x_min, x_max = self.plot_widget.viewRange()[0]
        window_size = x_max - x_min
        new_window_size = max(10, window_size * 0.9)  # Limit minimum window size
        center = (x_min + x_max) / 2
        self.plot_widget.setXRange(center - new_window_size / 2, center + new_window_size / 2, padding=0)

    def zoom_out(self):
        # Zoom out by adjusting x-axis limits (increase window size)
        x_min, x_max = self.plot_widget.viewRange()[0]
        window_size = x_max - x_min
        new_window_size = window_size * 1.1  # Increase window size by 10%
        center = (x_min + x_max) / 2
        self.plot_widget.setXRange(center - new_window_size / 2, center + new_window_size / 2, padding=0)

    def start_animation(self):
        # Calculate the animation interval based on the speed
        interval = int(1000 / self.animation_speed)  # Convert the interval to an integer
        self.timer.start(interval)
        self.animation_running = True
        self.start_button.setChecked(False)
        self.start_button.setText('Stop Animation')


    def stop_animation(self):
        self.timer.stop()
        self.animation_running = False
        self.start_button.setChecked(True)
        self.start_button.setText('Play Animation')

    def toggle_animation(self):
        if self.animation_running:
            self.stop_animation()
        else:
            self.start_animation()

    def move_left(self):
        # Move the visible range left by 50 data points
        x_min, x_max = self.plot_widget.viewRange()[0]
        x_min -= 50
        x_max -= 50
        self.plot_widget.setXRange(x_min, x_max)

    def move_right(self):
        # Move the visible range right by 50 data points
        x_min, x_max = self.plot_widget.viewRange()[0]
        x_min += 50
        x_max += 50
        self.plot_widget.setXRange(x_min, x_max, padding=0)


    def load_new_csv(self):
        # Open a file dialog to select a file with supported extensions
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Data File", "", "CSV Files (*.csv);;EDF Files (*.edf);;DAT Files (*.dat)", options=options
        )

        if file_path:
            file_extension = file_path.split('.')[-1]
            if file_extension.lower() == 'csv':
                # Load the CSV file containing signal data
                df = pd.read_csv(file_path)
            elif file_extension.lower() == 'edf':
                try:
                    # Load the EDF file using pyedflib
                    f = pyedflib.EdfReader(file_path)
                    num_signals = f.signals_in_file
                    signal_data = []
                    for i in range(num_signals):
                        signal_data.append(f.readSignal(i)[:N])
                    f.close()
                    
                    # Convert the EDF data to a DataFrame
                    df = pd.DataFrame(signal_data).T
                except Exception as e:
                    print(f"Error loading EDF file: {str(e)}")
                    return
            elif file_extension.lower() == 'dat':
                try:
                    # Load the DAT file as binary
                    with open(file_path, 'rb') as dat_file:
                        # Read the binary data
                        binary_data = dat_file.read()
                    
                    # Assuming the data is a series of floats, you can unpack it like this
                    # Adjust the struct format string according to your data format
                    import struct
                    data_format = 'f' * (len(binary_data) // struct.calcsize('f'))
                    dat_data = struct.unpack(data_format, binary_data)

                    # Create a single-column DataFrame from DAT data
                    df = pd.DataFrame(dat_data)
                except Exception as e:
                    print(f"Error loading DAT file: {str(e)}")
                    return
            else:
                # Unsupported file format
                return

            # Extract the signal data
            loaded_signal = df.iloc[:N, 0].tolist()
            return loaded_signal

    # Adding a new signal to the view
    def add_new_signal(self):
        #Add legend to the PlotWidget
        self.plot_widget.addLegend()
        
        # Load data from CSV file
        signal_data = self.load_new_csv() 
        
        # Assign a random color from colors list
        curve_color = random.choice(self.colors_list)
        
        # Create the signal object and add it to PlotWidget
        signal = pg.PlotCurveItem (signal_data, pen = curve_color, name = curve_color + "_Signal", clickable = True )
        
        self.plot_widget.addItem(signal)
        
        
        # plot_item = self.plot_widget.getPlotItem()
        # plot_item.setLabel('bottom', 'Time')
        # plot_item.setLabel('left', 'Amplitude')
        # plot_item.plot(pen='g')  # Create a new plot in the PlotItem

        # self.loaded_signals.append(loaded_signal)
        # self.x.append([])
        # self.y.append([])
        self.start_animation()

        

def main():
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window.setGeometry(100, 100, 1000, 600)
    main_window.setWindowTitle('ECG Signal Animation')

    signal_view1 = SignalView()
    signal_view2 = SignalView()

    # Create a container widget to hold the two SignalView widgets
    container = QWidget()
    container_layout = QHBoxLayout()
    container_layout.addWidget(signal_view1)
    container_layout.addWidget(signal_view2)
    container.setLayout(container_layout)

    main_window.setCentralWidget(container)

    main_window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


