import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QListWidget
app = QApplication([])

l = QListWidget()
l.addItem('Drag me')
l.setDragDropMode(l.DragOnly)
l.show()

win = pg.GraphicsLayoutWidget()
win.show()

def dragEnterEvent(ev):
    ev.accept()

win.dragEnterEvent = dragEnterEvent

plot = pg.PlotItem()
plot.setAcceptDrops(True)
win.addItem(plot)

def dropEvent(event):
    print("Got drop!")

plot.dropEvent = dropEvent


app.exec()