"""
=================================================================
======================== SignalMonitor.py =======================
=================================================================
"""


import typing
import sys
# from PyQt6 import QtCore, QtGui, QtWidgets, uic
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QGraphicsView, QDialog

from PyQt6 import uic


class myWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        load_ui("UiDesign.ui", self)

        # Add graphics view when 'Add view' button is pressed
        self.btn_addView.clicked.connect(self.addGraphicsView)

        # Open New File From the File Menubar
        self.ActionFile_OpenFile.triggered.connect(self.open_file_dialog)
        # self.open_shortcut.activated.connect(self.open_file_dialog)

        # Exit File From the File Menubar
        self.ActionFile_ExitFile.triggered.connect(self.close)
       
        # self.retranslateUi(myWindow)
        # QtCore.QMetaObject.connectSlotsByName(myWindow)


    # Function to add graphic view to signal display layout
    def addGraphicsView(self):
        new_graphics_view = QGraphicsView()
        self.lyt_SignalDisplay.addWidget(new_graphics_view)
    
    
    # Function to open the file select dialog
    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_dialog.exec()

    
    

        

app = QApplication(sys.argv)

#Create the main window and make it shown
homewindow = myWindow()
homewindow.show()

# Execute application
app.exec()