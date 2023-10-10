import sys
import pyqtgraph as pg
# from pyqtgraph.Qt import QtGui, QtCore
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QMainWindow

def create_plot():
    # Create a GraphicsLayoutWidget
    plot_widget = pg.GraphicsLayoutWidget()

    # Create some plot items
    plot_item1 = plot_widget.addPlot(row=0, col=0)
    plot_item2 = plot_widget.addPlot(row=1, col=0)

    # Add data to the plot items
    plot_item1.plot([1, 2, 3, 4, 5], [1, 3, 2, 4, 3], pen='r')
    plot_item2.plot([1, 2, 3, 4, 5], [2, 4, 3, 1, 2], pen='b')

    # Enable mouse interaction on each plot item
    plot_item1.setMouseEnabled(x=True, y=True)
    plot_item2.setMouseEnabled(x=True, y=True)

    return plot_widget

def main():
    # Create the QApplication
    app = QApplication(sys.argv)

    # Create the main window
    main_window = QMainWindow()
    main_window.setWindowTitle('Multiple Graphics Items Example')

    # Create the central widget and layout
    central_widget = QWidget()
    layout = QVBoxLayout()
    central_widget.setLayout(layout)

    # Create the plot and add it to the layout
    plot = create_plot()
    layout.addWidget(plot)

    # Set the central widget of the main window
    main_window.setCentralWidget(central_widget)

    # Show the main window
    main_window.show()

    # Start the event loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()