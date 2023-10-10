import sys

import pyqtgraph as pg
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGraphicsRectItem

pg.setConfigOption('background', 'k')
pg.setConfigOption('foreground', 'w')


class RemovableRect(QGraphicsRectItem):

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        """Remove me from the Scene"""
        self.scene().removeItem(self)


rect1 = RemovableRect(120, 120, 60, 60)
rect1.setPen(pg.mkPen((51, 51, 153), width=2))
rect1.setBrush(pg.mkBrush(51, 51, 153, 50))

rect2 = RemovableRect(200, 200, 80, 80)
rect2.setPen(pg.mkPen((51, 51, 153), width=2))
rect2.setBrush(pg.mkBrush(51, 51, 153, 50))

rect1.setFlag(rect1.ItemIsFocusable)
rect1.setFlag(rect1.ItemIsSelectable)
rect2.setFlag(rect2.ItemIsFocusable)
rect2.setFlag(rect2.ItemIsSelectable)


class win(pg.GraphicsLayoutWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('pyqtgraph GraphicsLayoutWidget')

        self.plt1 = self.addPlot(title='pyqtgraph PlotItem')

        self.plt1.addItem(rect1)
        self.plt1.addItem(rect2)
        self.plt1.disableAutoRange()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = win()
    w.show()
    sys.exit(app.exec_())