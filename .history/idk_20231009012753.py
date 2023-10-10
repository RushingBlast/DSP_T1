import sys
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QGraphicsRectItem
pg.setConfigOption('background', 'k')
pg.setConfigOption('foreground', 'w')

rect1 = QGraphicsRectItem(120, 120, 60, 60)
rect1.setPen(pg.mkPen((51, 51, 153), width=2))
rect1.setBrush(pg.mkBrush(51, 51, 153, 50))

rect2 = QGraphicsRectItem(200, 200, 80, 80)
rect2.setPen(pg.mkPen((51, 51, 153), width=2))
rect2.setBrush(pg.mkBrush(51, 51, 153, 50))

rect1.setFlag(rect1.ItemIsFocusable)
rect1.setFlag(rect1.ItemIsSelectable)
rect2.setFlag(rect2.ItemIsFocusable)
rect2.setFlag(rect2.ItemIsSelectable)

rect1.setZValue(1000)
rect2.setZValue(1000)

class win(pg.GraphicsLayoutWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('pyqtgraph GraphicsLayoutWidget')

        self.plt1 = self.addPlot(title='pyqtgraph PlotItem')
        self.plt1.setEnabled(False)

        self.plt1.addItem(rect1)
        self.plt1.addItem(rect2)
        self.plt1.disableAutoRange()

    def mousePressEvent(self, event):
        #item = self.scene().itemAt(event.pos(), QtGui.QTransform())
        item = self.itemAt(event.pos())
        print(item)
        #self.plt1.removeItem(item)
        self.scene().removeItem(item)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = win()
    w.show()
    sys.exit(app.exec_())
    