import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import numpy as np
import threading
import time

class LivePlotWidget(pg.GraphicsWindow):
    def __init__(self):
        super().__init__()

        self.plot_widget = self.addPlot()
        self.plot_curve = self.plot_widget.plot()
        self.data = np.zeros(100)  # Initial data

    def update_plot(self, new_data):
        self.data = np.concatenate((self.data[1:], [new_data]))
        self.plot_curve.setData(self.data)

    def start_data_acquisition(self):
        # Simulated data acquisition in a separate thread
        def data_acquisition_thread():
            while True:
                # Simulate data acquisition
                new_data = np.random.rand()
                # Emit signal to update the plot in the main GUI thread
                QtCore.QMetaObject.invokeMethod(
                    self, 'update_plot', QtCore.Qt.QueuedConnection, QtCore.Q_ARG(float, new_data)
                )
                time.sleep(0.1)  # Simulated delay between data points

        # Start the data acquisition thread
        self.data_thread = threading.Thread(target=data_acquisition_thread)
        self.data_thread.start()


if __name__ == '__main__':
    app = QtGui.QApplication([])
    plot_widget = LivePlotWidget()
    plot_widget.show()

    plot_widget.start_data_acquisition()

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()