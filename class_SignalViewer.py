import sys
import random
from PyQt5 import QtCore, QtGui
import pandas as pd
import numpy as np
import pyqtgraph as pg
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
from PyQt5.QtGui import QIcon
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
import datetime
import uuid
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Image, Spacer, PageBreak, PageTemplate, Frame, Paragraph, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors


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
        
        # Initialize the screenshots list
        self.screenshots = []

        self.animation_running = False
        self.x_values = [[]]
        self.y_values = [[]]
        self.current_index = 0
        self.x_min = 0
        self.x_max = fixed_window_size  # Initially set x_max to fixed_window_size
        self.loaded_signals = []  # List to store loaded signal data
        self.colors_list = ['b', 'r', 'g', 'c', 'm', 'y']  # List of colors to assign to signals
        self.signal_ranges = [(-1, 1), (1, 3), (3, 5), (5, 7), (7, 9), (9, 11), (11, 13), (13, 15), (15, 17), (17, 19),
                              (19, 21), (21, 23), (23, 25)]  # List of signal ranges

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
        # self.plot_widget = pg.PlotWidget()
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel('bottom', 'Time')
        self.plot_widget.setLabel('left', 'Amplitude')
        # Disable mouse panning until a signal is added
        self.plot_widget.setMouseEnabled(x=False, y=False)
        
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
        
        self.capture_button = QPushButton('Capture Screenshot', self)
        self.capture_button.clicked.connect(self.capture_screenshot)
        button_layout.addWidget(self.capture_button)
        
        # Create a button for saving screenshots as a PDF
        self.save_pdf_button = QPushButton('Save Screenshots as PDF', self)
        self.save_pdf_button.clicked.connect(self.save_screenshots_as_pdf)
        button_layout.addWidget(self.save_pdf_button)

        
        
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
        
        # Set timer for update function
        self.timer = QTimer(self)
        self.timer.stop()
        self.timer.timeout.connect(self.update)
        self.animation_speed = 100  # Default speed
    
    # Update the animation speed based on the slider value
    def update_speed(self):
            self.animation_speed = self.speed_slider.value()
            if self.animation_running:
                self.start_animation()  # Restart the animation with the updated speed

    # Function to clean the plotwidget and reset self.x_values[], self.y_values[] and Current_index
    def clean_plot(self):
        self.plot_widget.clear()

    
    
    # Update function for animated signal playback
    def update(self):
        if self.loaded_signals:
            if self.current_index < len(self.loaded_signals[0]):
                for i in range(len(self.loaded_signals)):
                    self.y_values[i].append(self.loaded_signals[i][self.current_index])
                    self.x_values[i].append(self.current_index)

                    if self.current_index >= self.x_max:
                        self.x_min += 1
                        self.x_max += 1

                    # Normalize the signal to be between its specified range
                    min_range, max_range = self.signal_ranges[i]
                    max_value = max(abs(max(self.y_values[i])), abs(min(self.y_values[i])))
                    if max_value != 0:
                        self.y_values[i][-1] = min_range + ((self.y_values[i][-1] / max_value) * (max_range - min_range))
                self.current_index += 1
            else:
                # All signals are done, reset
                self.current_index = 0
                for i in range(len(self.loaded_signals)):
                    self.x_values[i] = []
                    self.y_values[i] = []

        self.plot_widget.clear()
        for i in range(len(self.loaded_signals)):
            # Use different colors for each signal
            color = self.colors_list[i % len(self.colors_list)]
            plotted_signal = self.plot_widget.plot(self.x_values[i], self.y_values[i], pen=color, name=f'Signal {i + 1}', clickable = True)
            plotted_signal.sigClicked.connect(self.return_selected_signal)
        self.plot_widget.setXRange(self.x_min, self.x_max, padding=0)
        QApplication.processEvents()
        if not self.animation_running:
            self.start_animation()


    

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
          
            # Reset the x and y lists for the new signal
            self.x_values.append([])
            self.y_values.append([])

            self.loaded_signals.append(loaded_signal)

            plot_item = self.plot_widget.getPlotItem()
            plot_item.setLabel('bottom', 'Time')
            plot_item.setLabel('left', 'Amplitude')

        self.start_animation()


    # Returns Selected Signal from plot
    def return_selected_signal(self):
        print('Signal Clicked!')
        # selected_signal = self


    # Adding a new signal to the view
    def add_new_signal(self):
        self.load_new_csv() 
               
    # Capture a snapshot of plotwidget
    def capture_screenshot(self):
        screenshot = QtGui.QPixmap(self.grab())
        self.screenshots.append(screenshot)
               
 # Saving screenshot as pdf
    def save_screenshots_as_pdf(self):
        if not self.screenshots:
            return  # No screenshots to save

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4().hex[:8])  # Generate a unique identifier
        pdf_filename = f"report_{timestamp}_{unique_id}.pdf"

        # Create a SimpleDocTemplate with A4 size and specified margins
        doc = SimpleDocTemplate(pdf_filename, pagesize=A4,
                                leftMargin=0.5 * inch, rightMargin=0.5 * inch,
                                topMargin=0.5 * inch, bottomMargin=0.5 * inch)

        # Create a list to hold the elements (screenshots) for the PDF
        elements = []

        screenshot_width = 5 * inch  # Adjust the width as desired
        screenshot_height = 2 * inch  # Adjust the height as desired

        # Split the screenshots into groups of four
        grouped_screenshots = [self.screenshots[i:i + 4] for i in range(0, len(self.screenshots), 4)]

        for group in grouped_screenshots:
            # Create a list to hold the elements for each group of four screenshots
            group_elements = []
            group_elements.append(Spacer(0, 38))  # Add spacing before images in the beginning of each page
            for screenshot in group:
                # Add the image to the group elements list
                image_path = self.save_pixmap_as_image(screenshot)
                image = Image(image_path, width=screenshot_width, height=screenshot_height)
                group_elements.append(image)
                group_elements.append(Spacer(0, 30))  # Add spacing under each image

            # Add the group elements to the main elements list
            elements.extend(group_elements)

            # Add a page break after each group of four screenshots
            elements.append(PageBreak())

        # Define a function to draw the page number
        def draw_page_number(canvas, doc):
            page_num = canvas.getPageNumber()
            text = f"Page {page_num}"
            canvas.saveState()
            canvas.setFont("Helvetica", 10)
            canvas.setFillColor(colors.black)
            canvas.drawRightString(doc.pagesize[0] - 20, 20, text)
            canvas.restoreState()

            # Draw a box page border
            canvas.setStrokeColor(colors.black)
            canvas.setLineWidth(1)
            canvas.rect(doc.leftMargin, doc.bottomMargin,
                        doc.pagesize[0] - doc.leftMargin - doc.rightMargin,
                        doc.pagesize[1] - doc.bottomMargin - doc.topMargin,
                        stroke=True, fill=False)

        # Add the function to the SimpleDocTemplate
        doc.build(elements, onFirstPage=draw_page_number, onLaterPages=draw_page_number)

    # Saving the QPixmap object as a temporary PNG image file
    def save_pixmap_as_image(self, pixmap):
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        pixmap.save(temp_file.name, 'PNG')
        temp_file.close()
        return temp_file.name
        


    

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


