from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QGraphicsView, QDialog, QGridLayout, QShortcut
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QKeySequence
import numpy as np
from class_SignalViewer import class_signal_viewer
import sys

class main_window(QMainWindow):
    def __init__(self):
        super(main_window, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.linking_enabled = False
        # Used to handle unlinking the x axis during signal playback
        self.link_x_range_of_views = False

        self.activeWidget = None
        
        # Creating and setting menu bar
        menuBar = self.menuBar()
        self.setMenuBar(menuBar)
        
        # Create Signals menu
        signalMenu = QtWidgets.QMenu("&File", self)
        menuBar.addMenu(signalMenu)
        
        # Add open action to File Menu
        self.openAction = QtWidgets.QAction("&Open", self)
        signalMenu.addAction(self.openAction)
        
        # Adding rename action to File Menu
        self.renameAction = QtWidgets.QAction("&Rename", self)
        signalMenu.addAction(self.renameAction)

        # Adding Export action to File Menu
        self.exportAction = QtWidgets.QAction("&Export PDF", self)
        signalMenu.addAction(self.exportAction)

        self.setMinimumSize(1200, 600)

        self.container = QWidget()
        self.layout = QtWidgets.QHBoxLayout()

        self.signal_view_1 = class_signal_viewer(Qt.Key_O, Qt.Key_Z, Qt.Key_X, Qt.Key_C, Qt.Key_P, Qt.Key_R, Qt.Key_A, Qt.Key_D, Qt.Key_S)
        self.signal_view_2 = class_signal_viewer(QKeySequence('shift+O'), QKeySequence('shift+Z'), QKeySequence('shift+X'), QKeySequence('shift+C'), QKeySequence('shift+P'), QKeySequence('shift+R'), QKeySequence('shift+A'), QKeySequence('shift+D'), QKeySequence('shift+S'))
        self.layout.addWidget(self.signal_view_1)
        self.layout.addWidget(self.signal_view_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.addLayout(self.layout)
        self.setCentralWidget(self.container)
        self.container.setLayout(self.verticalLayout)
        self.signal_view_1.setFocus()

        # Setting up signal tranfer by linking views
        self.signal_view_1.btn_transfer.clicked.connect(lambda: self.signal_view_1.move_signal(self.signal_view_2))
        self.signal_view_2.btn_transfer.clicked.connect(lambda: self.signal_view_2.move_signal(self.signal_view_1))
    
        self.openAction.triggered.connect(self.signal_view_1.add_signal)
        self.exportAction.triggered.connect(lambda: self.signal_view_1.save_screenshots_as_pdf(self.signal_view_2.screenshots, self.signal_view_2.loaded_signals))
        self.renameAction.triggered.connect(self.rename_active_widget)
        
        
        self.signal_view_1.signal_emitter.sigPlotClicked.connect(self.signal_view_2.deselect_signal)
        self.signal_view_1.signal_emitter.sigPlotClicked.connect(lambda: self.mark_active_widget(self.signal_view_1))
        self.signal_view_2.signal_emitter.sigPlotClicked.connect(self.signal_view_1.deselect_signal)
        self.signal_view_2.signal_emitter.sigPlotClicked.connect(lambda: self.mark_active_widget(self.signal_view_2))
        
        self.signal_view_1.btn_link.clicked.connect(self.toggle_linking)
        self.signal_view_2.btn_link.clicked.connect(self.toggle_linking)
        
    
    def mark_active_widget(self, widget):
        self.activeWidget = widget
    
    def rename_active_widget(self):
        self.activeWidget.rename_selected_signal()




    # Function the toggles Linking the views
    def toggle_linking(self):
        # Toggle linking flag
        self.linking_enabled = not self.linking_enabled
        
        if self.linking_enabled:

            # set is_linked flag in both views
            self.signal_view_1.is_linked = self.signal_view_2.is_linked = True

            self.signal_view_1.view_widget.setXLink(self.signal_view_2.view_widget)
            self.signal_view_1.view_widget.setYLink(self.signal_view_2.view_widget)
        

         # Change UI for linked mode
            # self.signal_view_2.wgt_viewer_controls.setVisible(False)
            # self.verticalLayout.addWidget(self.signal_view_1.wgt_viewer_controls)
            self.signal_view_2.btn_add_signal.setEnabled(False)
            self.signal_view_2.btn_link.setEnabled(False)
            self.signal_view_2.btn_restart.setEnabled(False)
            self.signal_view_2.btn_start_pause.setEnabled(False)
            self.signal_view_2.btn_zoom_out.setEnabled(False)
            self.signal_view_2.btn_zoom_in.setEnabled(False)

        # Control view 2 with view 1's buttons
            # self.signal_view_1.btn_start_pause.clicked.disconnect(self.signal_view_1.toggle_animation)
            # self.signal_view_1.btn_start_pause.clicked.connect(self.linked_animation_playback)
            self.signal_view_1.btn_start_pause.clicked.connect(self.signal_view_2.toggle_animation)
            # self.signal_view_1.btn_play_pause_shortcut.activated.disconnect(self.signal_view_1.toggle_animation)
            # self.signal_view_1.btn_play_pause_shortcut.activated.connect(self.linked_animation_playback)

            self.signal_view_1.btn_clear.clicked.connect(self.signal_view_2.clear_signals)
            self.signal_view_1.btn_restart.clicked.connect(self.signal_view_2.reset_animation)
            self.signal_view_1.dial_speed.valueChanged.connect(lambda value: self.signal_view_2.dial_speed.setValue(value))
            
            # Toggle animation if either of the two plots was already running
            # self.signal_view_1.reset_animation()
            # self.signal_view_2.reset_animation()
            if self.signal_view_1.animation_running or self.signal_view_2.animation_running:
                self.signal_view_1.start_animation()
                self.signal_view_2.start_animation()
            
            # Setup both views
            self.signal_view_1.view_widget.setXRange(0, 1000)
            self.signal_view_1.view_widget.setYRange(-1.3, 1.3)

  

        else:
            # set is_linked flag in both views
            self.signal_view_1.is_linked = self.signal_view_2.is_linked = False
            
            self.signal_view_1.view_widget.setXLink(None)
            self.signal_view_1.view_widget.setYLink(None)

            # Return controls to normal
            self.signal_view_1.btn_restart.clicked.disconnect(self.signal_view_2.reset_animation)
            self.signal_view_1.btn_clear.clicked.disconnect(self.signal_view_2.clear_signals)
            
            self.signal_view_1.btn_start_pause.clicked.disconnect(self.signal_view_2.toggle_animation)
            
           
            # Return UI to normal
            self.signal_view_2.btn_restart.setEnabled(True)
            self.signal_view_2.btn_add_signal.setEnabled(True)
            self.signal_view_2.btn_link.setEnabled(True)
            self.signal_view_2.btn_start_pause.setEnabled(True)
            self.signal_view_2.btn_zoom_out.setEnabled(True)
            self.signal_view_2.btn_zoom_in.setEnabled(True)
            self.signal_view_1.dial_speed.valueChanged.disconnect()
            self.signal_view_1.dial_speed.valueChanged.connect(self.signal_view_1.update_speed)
            
            if self.signal_view_1.animation_running or self.signal_view_2.animation_running:
                self.signal_view_1.toggle_animation()
                self.signal_view_2.toggle_animation()
            

    
        QApplication.processEvents()
    
    # Handles animation playback in linked mode
    def linked_animation_playback(self):
        self.link_x_range_of_views = not self.link_x_range_of_views
        if self.link_x_range_of_views:

            self.signal_view_1.view_widget.sigYRangeChanged.connect(self.update_plot1_y_range)
            self.signal_view_2.view_widget.sigYRangeChanged.connect(self.update_plot2_y_range)
 
            self.signal_view_1.view_widget.sigXRangeChanged.connect(self.update_plot1_x_range)
            self.signal_view_2.view_widget.sigXRangeChanged.connect(self.update_plot2_x_range)
        else:
 
            self.signal_view_1.view_widget.sigYRangeChanged.connect(self.update_plot1_y_range)
            self.signal_view_2.view_widget.sigYRangeChanged.connect(self.update_plot2_y_range)
 
            self.signal_view_1.view_widget.sigXRangeChanged.disconnect(self.update_plot1_x_range)
            self.signal_view_2.view_widget.sigXRangeChanged.disconnect(self.update_plot2_x_range)
        self.signal_view_1.toggle_animation()
        self.signal_view_2.toggle_animation()
        
    def update_plot1_x_range(self):
        if self.linking_enabled:
            self.signal_view_2.view_widget.setXRange(*self.signal_view_1.view_widget.viewRange()[0], padding = 0)
    
    def update_plot2_x_range(self):
        if self.linking_enabled:    
            self.signal_view_1.view_widget.setXRange(*self.signal_view_2.view_widget.viewRange()[0], padding = 0)

    def update_plot1_y_range(self):
        if self.linking_enabled:    
            self.signal_view_2.view_widget.setYRange(*self.signal_view_1.view_widget.viewRange()[1], padding = 0)
    
    def update_plot2_y_range(self):
        if self.linking_enabled:    
            self.signal_view_1.view_widget.setYRange(*self.signal_view_2.view_widget.viewRange()[1], padding = 0)
        




app = QApplication(sys.argv)
win = main_window()
win.show()
app.exec()
