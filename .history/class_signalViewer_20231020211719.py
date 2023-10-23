from ui_signalViewer import Ui_Form
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QGraphicsView, QDialog, QGridLayout, QShortcut
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import pyqtgraph as pg
import numpy as np
import sys
from pyqtgraph import PlotWidget, plot, PlotDataItem
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile
import datetime
import uuid
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Image, Spacer, PageBreak, PageTemplate, Frame, Paragraph, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from pathlib import Path
import time



class class_signal_viewer(QWidget, Ui_Form):
    def __init__(self):
        super(class_signal_viewer, self).__init__()
        self.setupUi(self)
        self.btn_add_signal.setFocus()
        
        # Custom signal to emit when an empty space in the plot is clicked
        emptySpaceClicked = pyqtSignal()

################################################      CLASS VARIABLES      ################################################
    
        self.screenshots = []  # List to store the screenshots
        self.current_index= 0 # Index to iterate over the data to allow animated playback 
        self.selected_signal = any # Variable to store the selected signal object
        self.index_of_selected_signal = None # Store the Index of the selected signal in the loaded_signals list
        self.max_range = 0 #TODO - Check if this is needed anymore
        self.last_reached_index = 0 #TODO - Check if this is needed anymore
        self.animation_running = False # Flag to handle animated playback
        self.animation_speed = 1 # Value that determines the amount by which current_index is incremented
        self.x = [[]] #TODO - Check if this is needed anymore
        self.y = [[]] #TODO - Check if this is needed anymore
        self.loaded_signals = [] # list that holds the added signals
        self.colors_list = ["r", "b","g","y","m"] #TODO - Change to an actual random color generator
       
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
        # self.view_widget.setAutoPan(x = True, y = False)

################################################      SIGNAL CONNECTIONS      ################################################        

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

# Capture_Screenshots
        self.btn_snapshot.clicked.connect(lambda: self.capture_screenshot(self.view_widget))

# Save Screenshots as PDF
        self.btn_save.clicked.connect(self.save_screenshots_as_pdf)
        self.btn_save.clicked.connect(self.msg_pdf_created)

# Change signal color
        self.btn_change_color.clicked.connect(self.change_signal_color)

# EMPTY SPACE CLICKED IN PLOT
        # self.view_widget.sigMouseClicked.connect(self.deselect_signal)
        # self.view_widget.sigMouseReleased.connect(self.deselect_signal)

# SPEED CONTROL USING DIAL
        self.dial_speed.valueChanged.connect(self.update_speed)




################################################      CLASS FUNCTIONS      ################################################


#TODO - Add the extra formats (?)
#TODO - Normalize Data on input (?)

# Read csv files and save them in a list
    def read_signal_file(self ):
        file_dialog = QFileDialog()
        file_dialog.exec()
        filename = file_dialog.selectedFiles().pop()
        path = str(Path(filename))
        pandas_data = pd.read_csv(path).iloc[:, 0]
        data = pandas_data.to_numpy()
        return data
    
# Appends a PlotDataItem to loaded_signals
    def add_to_loaded_signals(self, new_signal = pg.PlotDataItem):
        self.loaded_signals.append(new_signal)
        
# Returns the object's loaded_signals list
    def get_loaded_signals(self):
        return self.loaded_signals

# Change color of selected signal
    def change_signal_color(self, new_color):
        new_color = QtWidgets.QColorDialog.getColor()
        self.loaded_signals[self.index_of_selected_signal].color = new_color
        self.loaded_signals[self.index_of_selected_signal].setPen(new_color)
        

# Rename selected signal
    def rename_selected_signal(self):
        pass


# Handle clicking in an empty space to deselect signals
    def deselect_signal(self):
        if len(self.loaded_signals) != 0: # Check if there are signals loaded
            # Iterate over loaded signals, setting their width to zero to 'deselct'
            for signal in self.loaded_signals:
                signal.setPen(signal.color, width = 0)
            self.selected_signal = any
            self.index_of_selected_signal = None


# Return Clicked signal
    def return_clicked_signal(self):
        self.selected_signal = self.sender()
        self.index_of_selected_signal = self.loaded_signals.index(self.sender())
        
        
        # TODO -  Remove this
        signal_name = self.selected_signal.opts["name"]
        print(f"selected {signal_name}")
        print(f"Index of selected signal is: {self.index_of_selected_signal}")
        
        # Iterate over loaded_signals to handle highlighting the selected signal
        for signal in self.loaded_signals:
            # Find the selected 
            if self.loaded_signals.index(signal) != self.index_of_selected_signal:
                signal.setPen(signal.color, width= 0)
            else:
                signal.setPen(signal.color, width= 5)

# Remove Signal from Plot
    def remove_selected_signal(self):
        self.view_widget.removeItem(self.loaded_signals[self.index_of_selected_signal])
        self.view_widget.loaded_signals.remove(self.loaded_signals[self.index_of_selected_signal])
        #TODO - Remove This
        print(len(self.loaded_signals))



# TODO - Add something to handle a signal's data coming to an end
#TODO - Add Plot scrolling effect
# Update plot widget
    def update(self):
        if self.loaded_signals:
            # Iterates over each signal in loaded signals and extends data by current_index
            for curve in self.loaded_signals:
                curve.setData(curve.original_data[0: self.current_index])              
                
            self.current_index += int(self.animation_speed) # Convert the speed value to integer
            QApplication.processEvents()



#TODO - Send over the current index data along with the transfer
# Move selected signal to another PlotWidget
    def move_signal(self, target_widget):
        if self.selected_signal:
            
            target_widget.view_widget.addLegend() # Ensure a legend is added to the target widget
            self.selected_signal.setPen(self.selected_signal.color, width = 0) # 'Unselect' the signal
            
            # Clone the selected signal and append it to the target widget's 'Loaded signals'
            sent_signal = pg.PlotDataItem(x = self.selected_signal.getData()[0],y= self.selected_signal.getData()[1] , pen = self.selected_signal.opts['pen'], name = self.selected_signal.opts['name'], clickable = True )
            sent_signal.color = self.selected_signal.color # Assigns proprety 'color' which contains original color of signal 
            sent_signal.original_data = self.selected_signal.original_data # Assigns property 'original_data' 
            sent_signal.sigClicked.connect(target_widget.return_clicked_signal)
            
            # Remove the signal from the owner widget (self)
            self.loaded_signals.pop(self.index_of_selected_signal)
            self.view_widget.removeItem(self.selected_signal)
            
            # Add the Clone to the target widget and set range automatically
            target_widget.add_to_loaded_signals(sent_signal)
            target_widget.view_widget.addItem(sent_signal)
            target_widget.view_widget.autoRange()
            self.selected_signal = None # Empty the selected_signal variable
            self.index_of_selected_signal = None
            
            # Transfer current_index from sender widget to receiver widget
            target_widget.current_index = self.current_index
            
            # If Target widget didn't have any loaded signals: enable mouse controls after moving one
            target_widget.view_widget.setMouseEnabled(x=True, y=True)
            target_widget.btn_zoom_in.setEnabled(True)
            target_widget.btn_zoom_out.setEnabled(True)

            # Recenter both widgets
            target_widget.view_widget.autoRange()
            self.view_widget.autoRange()


#TODO - Enhance color assignment

#TODO - Make animation play automatically after adding signal
# Add signals
    def add_signal(self):
        self.view_widget.addLegend()
        curve_color = random.choice(self.colors_list)
        
        data = self.read_signal_file()
        signal = pg.PlotDataItem(data, pen = curve_color, name = curve_color +"_Signal",clickable=True)
        signal.color = curve_color
        # Initialize loaded signal
        signal.original_data = data
        # self.loaded_signals.append(signal)
        self.add_to_loaded_signals(signal)
        self.view_widget.addItem(signal)
        signal.sigClicked.connect(self.return_clicked_signal)
        
        self.view_widget.autoRange()

        # Enable plot widget mouse controls
        self.view_widget.setMouseEnabled(x=True, y=True)
        self.btn_zoom_in.setEnabled(True)
        self.btn_zoom_out.setEnabled(True)
        self.view_widget.setLimits(xMin=0)
        self.horizontalScrollBar.valueChanged.connect(lambda value: self.view_widget.setXRange(value, value + 10))
        self.verticalScrollBar.valueChanged.connect(lambda value: self.view_widget.setYRange(value, value + 10))        


# Update animation speed
    def update_speed(self):
        self.animation_speed = self.dial_speed.value()
        self.lbl_speed.setText(f"Speed: {self.animation_speed}")

# Starts signal playback
    def start_animation(self):
        # Calculate the animation interval based on the speed
        # interval = int(1000 / self.animation_speed)# Convert the interval to an integer
        self.timer.start(1)
        self.animation_running = True
        self.btn_start_pause.setChecked(False)
        self.btn_start_pause.setText('Stop Animation')

        # Auto range the view widget
        # self.view_widget.autoRange()



# Stops signal playback
    def stop_animation(self):
        self.timer.stop()
        self.animation_running = False
        self.btn_start_pause.setChecked(True)
        self.btn_start_pause.setText('Play Animation')

# Toggle signal playback
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



# Clear signals
    def clear_signals(self):
        # Clear the PlotWidget and the loaded_signals list and reset current_index
        self.view_widget.clear()
        self.loaded_signals.clear()
        self.current_index = 0



# Capture screenshot in view 1
    def capture_screenshot(self, widget):
        screenshot = QtGui.QPixmap(widget.grab())
        self.screenshots.append(screenshot)



# Show a QMessage box notifying a pdf was created
    def msg_pdf_created(self):
        msg = QtWidgets.QMessageBox(title= "PDF Created", text= "PDF file was created successfully", buttons= None)
        msg.exec_()
        time.sleep(2)
        msg.close()



# Saving screenshot as pdf
    def save_screenshots_as_pdf(self):
        if not self.screenshots:
            return # No screenshots to save

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4().hex[:8]) # Generate a unique identifier
        pdf_filename = f"report_{timestamp}_{unique_id}.pdf"

        # Create a SimpleDocTemplate with A4 size and specified margins
        doc = SimpleDocTemplate(pdf_filename, pagesize=A4,
                                leftMargin=0.5 * inch, rightMargin=0.5 * inch,
                                topMargin= 0.5 * inch, bottomMargin=0.5 * inch)

        # Create a list to hold the elements (screenshots) for the PDF
        elements = []

        screenshot_width = 4 * inch # Adjust the width as desired
        screenshot_height = 2 * inch # Adjust the height as desired

        # Split the screenshots into groups of four
        grouped_screenshots = [self.screenshots[i:i+4] for i in range(0, len(self.screenshots), 4)]

        for group in grouped_screenshots:
            # Create a list to hold the elements for each group of four screenshots
            group_elements = []
            group_elements.append(Spacer(0, 38)) # Add spacing before images in the beginning of each page
            for screenshot in group:
                # Add the image to the group elements list
                image_path = self.save_pixmap_as_image(screenshot)
                image = Image(image_path, width=screenshot_width, height=screenshot_height)
                group_elements.append(image)
                group_elements.append(Spacer(0, 30)) # Add spacing under each image

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
    


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
