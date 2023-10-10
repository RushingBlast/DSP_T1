import sys
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
    QHBoxLayout,
    QFileDialog,
)

pg.QtGui.QShortcut
fixed_window_size = 300  # Set the initial fixed window size
# Initialize some variables
N = 10000  # Number of data points (adjust as needed)
t = np.linspace(0, N - 1, N)
y = np.zeros(N)
frame_times = np.zeros(N)  # Add this attribute to store frame times


class SignalView(QWidget):
    def __init__(self, play_pause_key, move_left_key, move_right_key, load_csv_key, zoom_in_key, zoom_out_key, parent=None):
        super().__init__(parent)

        self.x = []
        self.y = []
        self.current_index = 0
        self.x_min = 0
        self.x_max = fixed_window_size  # Initially set x_max to fixed_window_size
        self.loaded_signals = []  # List to store loaded signal data

        # Create shortcuts
        self.play_pause_shortcut = pg.QtGui.QShortcut(play_pause_key, self)
        self.play_pause_shortcut.activated.connect(self.toggle_animation)

        self.move_left_shortcut = pg.QtGui.QShortcut(move_left_key, self)
        self.move_left_shortcut.activated.connect(self.move_left)

        self.move_right_shortcut = pg.QtGui.QShortcut(move_right_key, self)
        self.move_right_shortcut.activated.connect(self.move_right)

        self.open_file_shortcut = pg.QtGui.QShortcut(load_csv_key, self)
        self.open_file_shortcut.activated.connect(self.load_new_csv)

        self.zoom_in_shortcut = pg.QtGui.QShortcut(zoom_in_key, self)
        self.zoom_in_shortcut.activated.connect(self.zoom_in)

        self.zoom_out_shortcut = pg.QtGui.QShortcut(zoom_out_key, self)
        self.zoom_out_shortcut.activated.connect(self.zoom_out)

        self.initUI()

    def initUI(self):
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel('bottom', 'Time')
        self.plot_widget.setLabel('left', 'Amplitude')

        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)

        button_layout = QHBoxLayout()
        self.start_button = QPushButton('Stop Animation')
        self.start_button.setCheckable(True)  # Make the button checkable (toggle)
        self.start_button.clicked.connect(self.toggle_animation)
        button_layout.addWidget(self.start_button)

        self.left_button = QPushButton('Move Left')
        self.left_button.clicked.connect(self.move_left)
        button_layout.addWidget(self.left_button)

        self.right_button = QPushButton('Move Right')
        self.right_button.clicked.connect(self.move_right)
        button_layout.addWidget(self.right_button)

        # Add a button to load a new CSV file
        self.load_button = QPushButton('Load CSV')
        self.load_button.clicked.connect(self.load_new_csv)
        button_layout.addWidget(self.load_button)

        self.zoom_in_button = QPushButton('Zoom In')
        self.zoom_in_button.clicked.connect(self.zoom_in)
        button_layout.addWidget(self.zoom_in_button)

        self.zoom_out_button = QPushButton('Zoom Out')
        self.zoom_out_button.clicked.connect(self.zoom_out)
        button_layout.addWidget(self.zoom_out_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.counter = count(0, 1)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.animation_running = True  # Flag to track animation state
        self.start_animation()

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
        self.timer.start(1)
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
        self.plot_widget.setXRange(x_min, x_max, padding=0)

    def move_right(self):
        # Move the visible range right by 50 data points
        x_min, x_max = self.plot_widget.viewRange()[0]
        x_min += 50
        x_max += 50
        self.plot_widget.setXRange(x_min, x_max, padding=0)

    def load_new_csv(self):
        # Open a file dialog to select a CSV file
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open CSV File", "", "CSV Files (*.csv)", options=options
        )

        if file_path:
            # Load the CSV file containing ECG signals
            df = pd.read_csv(file_path)

            # Extract the ECG data and set the new fixed_window_size based on the loaded data
            self.loaded_signals.append(df.iloc[:N, 0].tolist())
            self.x.append([])
            self.y.append([])


def main():
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window.setGeometry(100, 100, 1000, 600)
    main_window.setWindowTitle('ECG Signal Animation')

    # Create two instances of SignalView with different shortcuts
    signal_view1 = SignalView(Qt.Key_Space, Qt.Key_Left, Qt.Key_Right, Qt.CTRL + Qt.Key_O, Qt.CTRL + Qt.Key_Up, Qt.CTRL + Qt.Key_Down)
    signal_view2 = SignalView(Qt.SHIFT + Qt.Key_Space, Qt.SHIFT + Qt.Key_Left, Qt.SHIFT + Qt.Key_Right, Qt.SHIFT + Qt.CTRL + Qt.Key_O, Qt.SHIFT + Qt.CTRL + Qt.Key_Up, Qt.SHIFT + Qt.CTRL + Qt.Key_Down)

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
