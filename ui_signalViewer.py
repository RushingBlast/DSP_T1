# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'p5.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(985, 565)
        self.gridLayout_3 = QtWidgets.QGridLayout(Form)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.wgt_viewer_controls = QtWidgets.QWidget(Form)
        self.wgt_viewer_controls.setObjectName("wgt_viewer_controls")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.wgt_viewer_controls)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.btn_restart = QtWidgets.QPushButton(self.wgt_viewer_controls)
        self.btn_restart.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/restart.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_restart.setIcon(icon)
        self.btn_restart.setIconSize(QtCore.QSize(25, 25))
        self.btn_restart.setObjectName("btn_restart")
        self.gridLayout.addWidget(self.btn_restart, 2, 1, 1, 1)
        self.btn_snapshot = QtWidgets.QPushButton(self.wgt_viewer_controls)
        self.btn_snapshot.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/scrrenshot.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_snapshot.setIcon(icon1)
        self.btn_snapshot.setIconSize(QtCore.QSize(25, 25))
        self.btn_snapshot.setObjectName("btn_snapshot")
        self.gridLayout.addWidget(self.btn_snapshot, 3, 2, 1, 1)
        self.lbl_speed = QtWidgets.QLabel(self.wgt_viewer_controls)
        self.lbl_speed.setMinimumSize(QtCore.QSize(101, 0))
        self.lbl_speed.setMaximumSize(QtCore.QSize(60, 20))
        self.lbl_speed.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_speed.setObjectName("lbl_speed")
        self.gridLayout.addWidget(self.lbl_speed, 3, 4, 1, 1, QtCore.Qt.AlignHCenter)
        self.btn_zoom_out = QtWidgets.QPushButton(self.wgt_viewer_controls)
        self.btn_zoom_out.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/zoom_out.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_zoom_out.setIcon(icon2)
        self.btn_zoom_out.setIconSize(QtCore.QSize(25, 25))
        self.btn_zoom_out.setObjectName("btn_zoom_out")
        self.gridLayout.addWidget(self.btn_zoom_out, 3, 1, 1, 1)
        self.btn_clear = QtWidgets.QPushButton(self.wgt_viewer_controls)
        self.btn_clear.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/clear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_clear.setIcon(icon3)
        self.btn_clear.setIconSize(QtCore.QSize(25, 25))
        self.btn_clear.setObjectName("btn_clear")
        self.gridLayout.addWidget(self.btn_clear, 1, 3, 1, 1)
        self.btn_change_color = QtWidgets.QPushButton(self.wgt_viewer_controls)
        self.btn_change_color.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/color.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_change_color.setIcon(icon4)
        self.btn_change_color.setIconSize(QtCore.QSize(25, 25))
        self.btn_change_color.setObjectName("btn_change_color")
        self.gridLayout.addWidget(self.btn_change_color, 2, 2, 1, 1)
        self.btn_transfer = QtWidgets.QPushButton(self.wgt_viewer_controls)
        self.btn_transfer.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/transfer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_transfer.setIcon(icon5)
        self.btn_transfer.setIconSize(QtCore.QSize(40, 25))
        self.btn_transfer.setObjectName("btn_transfer")
        self.gridLayout.addWidget(self.btn_transfer, 1, 2, 1, 1)
        self.btn_add_signal = QtWidgets.QPushButton(self.wgt_viewer_controls)
        self.btn_add_signal.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icons/add.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_add_signal.setIcon(icon6)
        self.btn_add_signal.setIconSize(QtCore.QSize(25, 25))
        self.btn_add_signal.setObjectName("btn_add_signal")
        self.gridLayout.addWidget(self.btn_add_signal, 1, 0, 1, 1)
        self.lbl_view = QtWidgets.QLabel(self.wgt_viewer_controls)
        self.lbl_view.setMaximumSize(QtCore.QSize(60, 20))
        self.lbl_view.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_view.setObjectName("lbl_view")
        self.gridLayout.addWidget(self.lbl_view, 0, 1, 1, 2, QtCore.Qt.AlignHCenter)
        self.btn_remove = QtWidgets.QPushButton(self.wgt_viewer_controls)
        self.btn_remove.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("icons/remove.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_remove.setIcon(icon7)
        self.btn_remove.setIconSize(QtCore.QSize(25, 25))
        self.btn_remove.setObjectName("btn_remove")
        self.gridLayout.addWidget(self.btn_remove, 1, 1, 1, 1)
        self.btn_link = QtWidgets.QPushButton(self.wgt_viewer_controls)
        self.btn_link.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("icons/link.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_link.setIcon(icon8)
        self.btn_link.setIconSize(QtCore.QSize(25, 25))
        self.btn_link.setObjectName("btn_link")
        self.gridLayout.addWidget(self.btn_link, 2, 3, 1, 1)
        self.dial_speed = QtWidgets.QDial(self.wgt_viewer_controls)
        self.dial_speed.setMinimum(1)
        self.dial_speed.setMaximum(100)
        self.dial_speed.setNotchesVisible(True)
        self.dial_speed.setObjectName("dial_speed")
        self.gridLayout.addWidget(self.dial_speed, 0, 4, 3, 1)
        self.btn_zoom_in = QtWidgets.QPushButton(self.wgt_viewer_controls)
        self.btn_zoom_in.setEnabled(True)
        self.btn_zoom_in.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("icons/zoom_in.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_zoom_in.setIcon(icon9)
        self.btn_zoom_in.setIconSize(QtCore.QSize(25, 25))
        self.btn_zoom_in.setObjectName("btn_zoom_in")
        self.gridLayout.addWidget(self.btn_zoom_in, 3, 0, 1, 1)
        self.btn_save = QtWidgets.QPushButton(self.wgt_viewer_controls)
        self.btn_save.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("icons/pdf.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_save.setIcon(icon10)
        self.btn_save.setIconSize(QtCore.QSize(25, 25))
        self.btn_save.setObjectName("btn_save")
        self.gridLayout.addWidget(self.btn_save, 3, 3, 1, 1)
        self.btn_start_pause = QtWidgets.QPushButton(self.wgt_viewer_controls)
        self.btn_start_pause.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("icons/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_start_pause.setIcon(icon11)
        self.btn_start_pause.setIconSize(QtCore.QSize(25, 25))
        self.btn_start_pause.setObjectName("btn_start_pause")
        self.gridLayout.addWidget(self.btn_start_pause, 2, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 2, 2)
        self.gridLayout_3.addWidget(self.wgt_viewer_controls, 1, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.view_widget = PlotWidget(Form)
        self.view_widget.setObjectName("view_widget")
        self.horizontalLayout.addWidget(self.view_widget)
        self.verticalScrollBar = QtWidgets.QScrollBar(Form)
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setInvertedAppearance(True)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.horizontalLayout.addWidget(self.verticalScrollBar)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalScrollBar = QtWidgets.QScrollBar(Form)
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")
        self.verticalLayout.addWidget(self.horizontalScrollBar)
        self.gridLayout_3.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.lbl_stats = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_stats.sizePolicy().hasHeightForWidth())
        self.lbl_stats.setSizePolicy(sizePolicy)
        self.lbl_stats.setMinimumSize(QtCore.QSize(0, 19))
        self.lbl_stats.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lbl_stats.setObjectName("lbl_stats")
        self.gridLayout_3.addWidget(self.lbl_stats, 2, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.lbl_speed.setText(_translate("Form", "Speed"))
        self.btn_zoom_out.setShortcut(_translate("Form", "Ctrl+Down"))
        self.btn_add_signal.setShortcut(_translate("Form", "Ctrl+O"))
        self.lbl_view.setText(_translate("Form", "View"))
        self.btn_zoom_in.setShortcut(_translate("Form", "Ctrl+Up"))
        self.btn_start_pause.setShortcut(_translate("Form", "Space"))
        self.lbl_stats.setText(_translate("Form", "No Signal Selected..."))
from pyqtgraph import PlotWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
