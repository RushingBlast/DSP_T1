import sys
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

def create_plot():
    # Create a PlotWidget
    plot_widget = pg.PlotWidget()

    # Create some plot items
    plot_item1 = plot_widget.plot([1, 2, 3, 4, 5], [1, 3, 2, 4, 3], pen='r')
    plot_item2 = plot_widget.plot([1, 2, 3, 4, 5], [2, 4, 3, 1, 2], pen='b')

    # Enable mouse interaction on each plot item
    plot_item1.setFlag(pg.PlotCurveItem.ItemIsMovable)
    plot_item1.setFlag(pg.PlotCurveItem.ItemIsSelectable)
    plot_item2.setFlag(pg.PlotCurveItem.ItemIsMovable)
    plot_item2.setFlag(pg.PlotCurveItem.ItemIsSelectable)

    return plot_widget



"""
def main():
    
    # Create the QApplication
    myapp = QApplication(sys.argv)

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
    sys.exit(myapp.exec_())

if __name__ == '__main__':
    main()"""

    
# # Create the QApplication
# myapp = QApplication(sys.argv)

# # Create the main window
# main_window = QMainWindow()
# main_window.setWindowTitle('Multiple Graphics Items Example')



# # Create the central widget and layout
# central_widget = QWidget()
# layout = QVBoxLayout()
# central_widget.setLayout(layout)

# # Set the central widget of the main window
# main_window.setCentralWidget(central_widget)


# # # Create the plot and add it to the layout
# # plot = create_plot()

# plot_widget = pg.PlotWidget()
# layout.addWidget(plot_widget)


# # Show the main window
# main_window.show()

# # Start the event loop
# sys.exit(myapp.exec_())

def main():
    app = QApplication(sys.argv)
    main = QMainWindow()
    
    central_widget = QWidget()
    layout = QVBoxLayout()
    central_widget.setLayout(layout)

    main.setCentralWidget(central_widget)
    # plot = pg.PlotWidget()

    # layout.addItem(plot)


    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()