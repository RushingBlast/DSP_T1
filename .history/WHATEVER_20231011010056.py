from new import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow


class mywindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        
        self.setupUi(self)
        

app = QApplication([])

window = mywindow()
window.show()

app.exec() 