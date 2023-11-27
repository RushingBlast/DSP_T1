from os import name

from sympy import Q
from ui_signalViewer import Ui_Form
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QGraphicsView, QDialog, QGridLayout, QShortcut
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
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

     
        
        




"""MAIN SIGNAL VIEWER WIDGET"""
class class_signal_viewer(QWidget, Ui_Form):
    def __init__(self,add_signal_btn, zoom_in_btn, zoom_out_btn, clear_btn, play_pause_btn, remove_btn, reset_btn, snapshot_btn, save_btn):
        super(class_signal_viewer, self).__init__()
        self.setupUi(self)
        self.btn_add_signal.setFocus()


################################################      CLASS VARIABLES      ################################################
        
        
        self.screenshots = []  # List to store the screenshots
        self.current_index= 0 # Index to iterate over the data to allow animated playback 
        self.selected_signal = any # Variable to store the selected signal object
        self.index_of_selected_signal = None # Store the Index of the selected signal in the loaded_signals lis
        self.animation_running = False # Flag to handle animated playback
        self.animation_speed = 1 # Value that determines the amount by which current_index is incremented
        self.is_linked = False # Flag to track linking status

        
        self.x_min = 0
        self.x_max = 1000
        
        self.loaded_signals = [] # list that holds the added signals
        self.colors_list = self.colors_list = [
                                                "red ", "blue ", "green", "yellow", "magenta",
                                                "cyan", "orange", "purple", "pink", "lime", "teal", "maroon", "indigo"
                                            ]

        # Set timer for update function
        self.timer = QtCore.QTimer(self)
        self.timer.stop()
        self.timer.timeout.connect(self.update)
        # self.animation_speed = 100  # Default speed
        self.signal_buttons_set_enabled(False)
        
################################################      SHORTCUTS      ################################################        
# ADD_SIGNAL_BTN_SHORTCUTS        
        self.btn_add_signal_shortcut = QShortcut(add_signal_btn, self)
        self.btn_add_signal_shortcut.activated.connect(self.add_signal)

# ZOOM_IN_BTN_SHORTCUTS
        self.btn_zoom_in_shortcut = QShortcut(zoom_in_btn, self)
        self.btn_zoom_in_shortcut.activated.connect(self.zoom_in)

# ZOOM_OUT_BTN_SHORTCUTS
        self.btn_zoom_out_shortcut = QShortcut(zoom_out_btn, self)
        self.btn_zoom_out_shortcut.activated.connect(self.zoom_out)

# CLEAR_BTN_SHORTCUTS
        self.btn_clear_shortcut = QShortcut(clear_btn, self)
        self.btn_clear_shortcut.activated.connect(self.clear_signals)

# PLAY/PAUSE_BTN_SHORTCUTS
        self.btn_play_pause_shortcut = QShortcut(play_pause_btn, self)
        self.btn_play_pause_shortcut.activated.connect(self.toggle_animation)

# REMOVE_BTN_SHORTCUTS
        self.btn_remove_shortcut = QShortcut(remove_btn, self)
        self.btn_remove_shortcut.activated.connect(self.remove_selected_signal)

# RESET_BTN
        self.btn_reset_shortcut = QShortcut(reset_btn, self)
        self.btn_reset_shortcut.activated.connect(self.reset_animation)

# Capture_Screenshots
        self.btn_snapshot_shortcut = QShortcut(snapshot_btn, self)
        self.btn_snapshot_shortcut.activated.connect(lambda: self.capture_screenshot(self.view_widget))

# Save Screenshots as PDF
        self.btn_save_shortcut = QShortcut(save_btn, self)
        self.btn_save_shortcut.activated.connect(self.save_screenshots_as_pdf)
        
################################################      VIEW DETAILS      ################################################        

        
        self.view_widget.setLabel('bottom', 'Time')
        self.view_widget.setLabel('left', 'Amplitude')
        self.view_widget.setXRange(0,11,0)
        self.view_widget.setYRange(-1.3, 1.3,0)
        self.view_widget.setLimits(yMin = -1.3, yMax = 1.3 )
        self.horizontalScrollBar.setVisible(False)
        self.verticalScrollBar.setVisible(False)
        self.view_widget.setMouseEnabled(x=False, y=False)
       
       # Disable buttons except for Add_signal
        self.btn_zoom_in.setEnabled(False)
        self.btn_zoom_out.setEnabled(False)
        self.btn_link.setEnabled(False)
        self.btn_save.setEnabled(False)
        self.btn_snapshot.setEnabled(False)
        self.lbl_speed.setText(f"Speed: {self.animation_speed}")

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

# RESET_BTN
        self.btn_restart.clicked.connect(self.reset_animation)

# Capture_Screenshots
        self.btn_snapshot.clicked.connect(lambda: self.capture_screenshot(self.view_widget))

# Save Screenshots as PDF
        self.btn_save.clicked.connect(self.save_screenshots_as_pdf)
        # self.btn_save.clicked.connect(self.msg_pdf_created)

# Change signal color
        self.btn_change_color.clicked.connect(self.change_signal_color)

# SPEED CONTROL USING DIAL
        self.dial_speed.valueChanged.connect(self.update_speed)




################################################      CLASS FUNCTIONS      ################################################


# Read csv files and save them in a list
    def read_signal_file(self):
        file_dialog = QFileDialog()
        file_dialog.exec()
        filename = file_dialog.selectedFiles().pop()
        path = str(Path(filename))
        pandas_data = pd.read_csv(path).iloc[:, 0]
        data = pandas_data.to_numpy()
        data_mean = np.mean(data)
        data_median = np.median(data)
        data_std = np.std(data)
        data_max = np.max(data)
        data_min = np.min(data)
        stats = (data_mean, data_median, data_std, data_max, data_min)
        return data , stats
    
# Appends a pg.PlotDataItem to loaded_signals
    def add_to_loaded_signals(self, new_signal =pg.PlotDataItem):
        self.loaded_signals.append(new_signal)
        
# Returns the object's loaded_signals list
    def get_loaded_signals(self):
        return self.loaded_signals
    

# Change color of selected signal
    def change_signal_color(self, new_color):
        if self.selected_signal:
            new_color = QtWidgets.QColorDialog.getColor()
            
            # Check if the new color is already in use by another signal
            color_in_use = False
            for signal in self.loaded_signals:
                if signal != self.selected_signal and signal.color == new_color:
                    color_in_use = True
                    break
            
            if not color_in_use:
                self.selected_signal.color = new_color
                self.selected_signal.setPen(new_color)
            else:
                QtWidgets.QMessageBox.warning(
                    self, "Color Already in Use",
                    "The selected color is already in use by another signal.",
                    QtWidgets.QMessageBox.Ok
                )

        

# Rename selected signal
    def rename_selected_signal(self):
        new_name, accept = QtWidgets.QInputDialog.getText(self, "Rename Signal", "Signal name: ")
        if new_name and accept:
            self.loaded_signals[self.index_of_selected_signal].opts['name'] = new_name 
            self.view_widget.addLegend().removeItem(self.selected_signal)
            self.view_widget.addLegend().addItem(self.selected_signal, new_name)
        self.deselect_signal()

            


# Handle clicking in an empty space to deselect signals
    def deselect_signal(self):
        if len(self.loaded_signals) != 0: # Check if there are signals loaded
            # Iterate over loaded signals, setting their width to zero to 'deselct'
            for signal in self.loaded_signals:
                signal.setPen(signal.color, width = 0)
            self.selected_signal = None
            self.index_of_selected_signal = None


# select Clicked signal
    def select_clicked_signal(self):
        
        self.signal_buttons_set_enabled(True) # Enable signal-dependent buttons

        #If the selected signal is clicked again: deselect and disable corresponding buttons
        if self.selected_signal == self.sender():
            print(f"Deselectd signal {self.selected_signal.opts['name']}")
            self.deselect_signal()
            self.signal_buttons_set_enabled(False) 
            return
        
        # self.selected_signal = self.sender()
        self.index_of_selected_signal = self.loaded_signals.index(self.sender()) # Get index of selected signal in loaded signal
        self.selected_signal = self.loaded_signals[self.index_of_selected_signal] # Store the selected signal in a variable to be reused

        self.stats_of_selected_signal()
        # Iterate over loaded_signals to handle highlighting the selected signal
        for signal in self.loaded_signals:
            # Find the selected 
            if self.loaded_signals.index(signal) != self.index_of_selected_signal:
                signal.setPen(signal.color, width= 0)
            else:
                signal.setPen(signal.color, width= 5)
       
# Function to enable/disable buttons that need a signal to be selected
    def signal_buttons_set_enabled(self, flag):
        self.btn_change_color.setEnabled(flag)
        self.btn_transfer.setEnabled(flag)
        self.btn_remove.setEnabled(flag)
        

# Remove Signal from Plot
    def remove_selected_signal(self):
        self.view_widget.removeItem(self.loaded_signals[self.index_of_selected_signal])
        self.view_widget.loaded_signals.remove(self.loaded_signals[self.index_of_selected_signal])

        self.signal_buttons_set_enabled(False)




# Update plot widget
    def update(self):
        if self.loaded_signals:
            # Iterates over each signal in loaded signals and extends data by current_index
            for curve in self.loaded_signals:
                curve.setData(curve.original_data[0: self.current_index])              
            
            if self.current_index > self.x_max:   
                self.x_max += int(self.animation_speed)
                self.x_min += int(self.animation_speed)    
                self.view_widget.setLimits(xMax = self.current_index)
            self.view_widget.setXRange(self.x_min, self.x_max)

            
            self.current_index += int(self.animation_speed) # Convert the speed value to integer
            QApplication.processEvents()



#TODO - Send over the current index data along with the transfer
# Move selected signal to another PlotWidget
    def move_signal(self, target_widget):
        if self.selected_signal:
            
            self.signal_buttons_set_enabled(False)
            
            target_widget.view_widget.addLegend() # Ensure a legend is added to the target widget
            self.selected_signal.setPen(self.selected_signal.color, width = 0) # 'Unselect' the signal
            
            # Clone the selected signal and append it to the target widget's 'Loaded signals'
            sent_signal = pg.PlotDataItem(x = self.selected_signal.getData()[0],y= self.selected_signal.getData()[1] , pen = self.selected_signal.opts['pen'], name = self.selected_signal.opts['name'], clickable = True, radius = 5)
            sent_signal.color = self.selected_signal.color # Assigns proprety 'color' which contains original color of signal 
            sent_signal.original_data = self.selected_signal.original_data # Assigns property 'original_data' 
            sent_signal.stats = self.selected_signal.stats
            sent_signal.sigClicked.connect(target_widget.select_clicked_signal)
            
            # Remove the signal from the owner widget (self)
            self.loaded_signals.pop(self.index_of_selected_signal)
            self.view_widget.removeItem(self.selected_signal)
            
            # Add the Clone to the target widget and set range automatically
            target_widget.add_to_loaded_signals(sent_signal)
            target_widget.view_widget.addItem(sent_signal)
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
            self.signal_buttons_set_enabled(False)

# Display Stats of selected signal in label in status bar
    def stats_of_selected_signal(self):
        if self.selected_signal:
            stats = self.selected_signal.stats
            self.lbl_stats.setText(f"Mean: {stats[0]}, Median: {stats[1]}, Std: {stats[2]}, Max: {stats[3]}, Min: {stats[4]}")


# Add signals
    def add_signal(self):
        self.view_widget.addLegend()
        curve_color = random.choice(self.colors_list)
        
        data, stats = self.read_signal_file()
        
        # Initialize loaded signal
        signal = pg.PlotDataItem(data, pen = curve_color, name = "Signal_"+ str(len(self.loaded_signals)) ,clickable=True , radius = 5)
        signal.color = curve_color # Holds the color assigned to the signal at creation
        signal.original_data = data # hold the original data of the signal
        
        # Holds Signal's data statistics.
        # (mean, median, std, max, min)
        signal.stats = stats
       
        self.add_to_loaded_signals(signal) #Adds the signal to the loaded_signals list
        self.view_widget.addItem(signal)
        signal.sigClicked.connect(self.select_clicked_signal)
        
        # Enable plot widget mouse controls
        self.view_widget.setMouseEnabled(x=True, y=True)
        self.btn_link.setEnabled(True)
        self.btn_zoom_in.setEnabled(True)
        self.btn_zoom_out.setEnabled(True)
        self.view_widget.setLimits(xMin=0)
        self.btn_save.setEnabled(True)
        self.btn_snapshot.setEnabled(True)      
                
        #If animation is not running, start_animation
        if not self.animation_running:
            self.toggle_animation()


# Update animation speed
    def update_speed(self):
        self.animation_speed = self.dial_speed.value()
        self.lbl_speed.setText(f"Speed: {self.animation_speed}") # Update label text to show speed value


# Starts signal playback
    def start_animation(self):            
        if not self.loaded_signals:
            return

        self.timer.start(1)
        self.animation_running = True
        self.btn_start_pause.setChecked(False)
        self.btn_start_pause.setIcon(QIcon('icons\pause.png'))

        min_x, max_x, min_y, max_y = self.find_data_range()

        if max_x - min_x > 10000:
            max_x = min_x + 10000

        # Set the view range to show the first 10,000 points
        self.view_widget.setXRange(min_x, max_x)
        # self.view_widget.setLimits(yMin = min_y, yMax = max_y )

        # Auto range the view widget
        self.view_widget.autoRange()

    # Function to find the data range of the loaded signals
    def find_data_range(self):
        if not self.loaded_signals:
            return 0, 0, 0, 0

        min_x = float('inf')
        max_x = float('-inf')
        min_y = float('inf')
        max_y = float('-inf')

        for signal in self.loaded_signals:
            x, y = signal.getData()
            if len(x) > 0:
                min_x = min(min_x, min(x))
                max_x = max(max_x, max(x))
                min_y = min(min_y, min(y))
                max_y = max(max_y, max(y))

        return min_x, max_x, min_y, max_y

# # Resets View Range to X= 0 : 100
#     def reset_view_range(self):
#         self.view_widget.setXRange(0 , 100)

# Reset Signal Playback
    def reset_animation(self):
        self.current_index = 0
        self.view_widget.setXRange(0, 1000)
        self.x_min = 0
        self.x_max = 1000

# Stops signal playback
    def stop_animation(self):
        self.timer.stop()
        self.animation_running = False
        self.btn_start_pause.setChecked(True)
        self.btn_start_pause.setIcon(QIcon('icons\play.png'))

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
        self.current_index = 0 # Reset current_index to reset playback
        self.signal_buttons_set_enabled(False)
        self.screenshots.clear() # Clear Screenshot queue
        if self.animation_running:
            self.toggle_animation()



# Capture screenshot in view 1
    def capture_screenshot(self, widget):
        screenshot = QtGui.QPixmap(widget.grab())
        self.screenshots.append(screenshot)



# Show a QMessage box notifying a pdf was created
    def msg_pdf_created(self):
        msg = QtWidgets.QMessageBox(self)
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setWindowTitle("PDF Created!")
        msg.setText("PDF file was created successfully")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok) 
        msg.exec()



# Saving screenshot as pdf
    def save_screenshots_as_pdf(self):
        if not self.screenshots:  # No screenshots to save
            error_msg = QtWidgets.QMessageBox(self)
            error_msg.setIcon(QtWidgets.QMessageBox.Critical)
            error_msg.setWindowTitle("Error!")
            error_msg.setText("No Screenshots to save!")
            error_msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            error_msg.exec()
            return
        try:
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
                group_elements.append(Spacer(0, 48)) # Add spacing before images in the beginning of each page
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
                
                # Add date/time
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                canvas.setFont("Helvetica", 10)
                canvas.drawString(20, 20, f"Exported on: {timestamp}")


                # Add headline
                if page_num == 1:
                    headline = "Report"
                    canvas.setFont("Helvetica-Bold", 22)
                    canvas.drawCentredString(doc.pagesize[0] / 2, doc.pagesize[1] - 70, headline)

                canvas.restoreState()

                # Draw a box page border
                canvas.setStrokeColor(colors.black)
                canvas.setLineWidth(1)
                canvas.rect(doc.leftMargin, doc.bottomMargin,
                            doc.pagesize[0] - doc.leftMargin - doc.rightMargin,
                            doc.pagesize[1] - doc.bottomMargin - doc.topMargin,
                            stroke=True, fill=False)

            # Add the statistics table to the last page
            elements.append(Spacer(0, 1))
            
            # Add the headline before the table
            headline_text = "Signal Statistics:"
            styles = getSampleStyleSheet()
            headline = Paragraph(headline_text, styles['Heading2'])
            elements.append(headline)
     
            elements.append(Spacer(0, 5))

            table_data = [[' Signal Name ', '   Mean   ', 'Standard Dev.', '  Duration  ', ' Max. Value ', ' Min. Value ']]
            # table_data.extend(add the data here)


            # Iterate over loaded signals to fill table            
            for signal in self.loaded_signals:
                table_data.extend([[signal.opts['name'], round(signal.stats[0], 2), round(signal.stats[2], 2), f"{len(signal.original_data)} ms", round(signal.stats[3], 2), round(signal.stats[4], 2)]])


            table = Table(table_data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))

            elements.append(table)
            
            # Add the function to the SimpleDocTemplate
            doc.build(elements, onFirstPage=draw_page_number, onLaterPages=draw_page_number)


        except: # Display notification that PDF couldn't be created
            failed_msg = QtWidgets.QMessageBox(self)
            failed_msg.setIcon(QtWidgets.QMessageBox.Critical)
            failed_msg.setWindowTitle("Error!")
            failed_msg.setText("Coudn't create PDF!")
            failed_msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            failed_msg.exec()
            return
        # Notification that PDF was created successfully
        self.msg_pdf_created()

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
