from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QGraphicsView, QDialog, QGridLayout, QShortcut
from PyQt5 import QtCore, QtGui, QtWidgets
from class_signalViewer import class_signal_viewer
import sys

class main_window(QMainWindow):
    def __init__(self):
        super(main_window, self).__init__()
        self.init_ui()

    def init_ui(self):

        # Test color
         # Creating and setting menu bar
        menuBar = self.menuBar()
        self.setMenuBar(menuBar)
        
        # Creating the File menu
        fileMenu = QtWidgets.QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        
        # Create Signals menu
        signalMenu = QtWidgets.QMenu("&Signal", self)
        menuBar.addMenu(signalMenu)
        
        # Creating and adding Action to Signal Menu
        self.colorAction = QtWidgets.QAction("&Color", self)
        signalMenu.addAction(self.colorAction)
        
        # Creating and adding Action to Signal Menu
        self.colorAction = QtWidgets.QAction("&Color", self)
        signalMenu.addAction(self.colorAction)
        

        self.container = QWidget()
        self.layout = QtWidgets.QHBoxLayout()
        signal_view_1 = class_signal_viewer()
        signal_view_2 = class_signal_viewer()
        self.layout.addWidget(signal_view_1)
        self.layout.addWidget(signal_view_2)
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)
        signal_view_1.setFocus()
        self.setMinimumSize(700, 500)

        # Setting up signal tranfer by linking views
        signal_view_1.btn_transfer.clicked.connect(lambda: signal_view_1.move_signal(signal_view_2))
        signal_view_2.btn_transfer.clicked.connect(lambda: signal_view_2.move_signal(signal_view_1))
        signal_1_loaded_signals = signal_view_1.get_loaded_signals
        signal_2_loaded_signals = signal_view_2.get_loaded_signals

"""

    # Function the toggles Linking the views
    def toggle_linking(self):
        self.linking_enabled = not self.linking_enabled
        
        # IF either of the views in playback. Start playback when linking
        if signal_viewer_1.animation_running or signal_viewer_2.animation_running:
            self.linked_animation_playback()
        if self.linking_enabled:
            self.linkAction.setText("Unlink")
            signal_viewer_1.start_button.clicked.disconnect(signal_viewer_1.toggle_animation)
            signal_viewer_1.start_button.clicked.connect(self.linked_animation_playback)
            # signal_viewer_2.start_button.clicked.connect(self.linked_animation_playback)
            signal_viewer_2.button_container.setVisible(False)
            signal_viewer_2.button_container.setEnabled(False)
            
            # Reset both views to prepare for linked playback
            signal_viewer_1.clean_plot()
            signal_viewer_2.clean_plot()
            signal_viewer_1.toggle_animation()
            signal_viewer_2.toggle_animation()
            
            minimum_x_max = np.minimum(signal_viewer_1.x_max, signal_viewer_2.x_max)
            signal_viewer_1.x_min = signal_viewer_2.x_min
            signal_viewer_1.x_max = signal_viewer_2.x_max = minimum_x_max
            signal_viewer_1.plot_widget.autoRange()
            
            
        else:
            self.linkAction.setText("Link")
            signal_viewer_1.start_button.clicked.disconnect(self.linked_animation_playback)
            signal_viewer_1.start_button.clicked.connect(signal_viewer_1.toggle_animation)
            signal_viewer_2.button_container.setVisible(True)
            signal_viewer_2.button_container.setEnabled(True)
            
        self.update_plot1_x_range()
        self.update_plot2_x_range()
        self.update_plot1_y_range()
        self.update_plot2_y_range()
        QApplication.processEvents()
    
    def linked_animation_playback(self):
        self.link_x_range_of_views = not self.link_x_range_of_views
        if self.link_x_range_of_views:
            signal_viewer_1.plot_widget.sigXRangeChanged.connect(self.update_plot1_x_range)
            signal_viewer_2.plot_widget.sigXRangeChanged.connect(self.update_plot2_x_range)
        else:
            
            signal_viewer_1.plot_widget.sigXRangeChanged.disconnect(self.update_plot1_x_range)
            signal_viewer_2.plot_widget.sigXRangeChanged.disconnect(self.update_plot2_x_range)
        signal_viewer_1.toggle_animation()
        signal_viewer_2.toggle_animation()
        
    def update_plot1_x_range(self):
        if self.linking_enabled:
            signal_viewer_2.plot_widget.setXRange(*signal_viewer_1.plot_widget.viewRange()[0], padding = 0)
    
    def update_plot2_x_range(self):
        if self.linking_enabled:    
            signal_viewer_1.plot_widget.setXRange(*signal_viewer_2.plot_widget.viewRange()[0], padding = 0)

    def update_plot1_y_range(self):
        if self.linking_enabled:    
            signal_viewer_2.plot_widget.setYRange(*signal_viewer_1.plot_widget.viewRange()[1], padding = 0)
    
    def update_plot2_y_range(self):
        if self.linking_enabled:    
            signal_viewer_1.plot_widget.setYRange(*signal_viewer_2.plot_widget.viewRange()[1], padding = 0)
        

"""


app = QApplication(sys.argv)
win = main_window()
win.show()
app.exec()
