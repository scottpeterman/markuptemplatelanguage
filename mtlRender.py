# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tfsmRender2.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

darkstyle = True

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDesktopWidget, QMessageBox
import json
import uuid
import os, sys
from pprint import pprint as pp
import mtl

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(965, 707)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.teSource = QtWidgets.QTextEdit(self.centralwidget)
        self.teSource.setGeometry(QtCore.QRect(20, 410, 501, 231))
        self.teSource.setObjectName("teSource")
        self.teSource.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.teSource.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.teSource.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)

        self.teTemplate = QtWidgets.QTextEdit(self.centralwidget)
        self.teTemplate.setGeometry(QtCore.QRect(20, 70, 901, 291))
        self.teTemplate.setObjectName("teTemplate")
        self.teTemplate.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.teTemplate.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.teTemplate.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)

        self.teResult = QtWidgets.QTextEdit(self.centralwidget)
        self.teResult.setGeometry(QtCore.QRect(560, 410, 371, 231))
        self.teResult.setObjectName("teResult")
        self.teResult.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.teResult.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.teResult.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)


        self.pbSample = QtWidgets.QPushButton(self.centralwidget)
        self.pbSample.setGeometry(QtCore.QRect(190, 370, 101, 27))
        self.pbSample.setObjectName("pbSample")

        # this clicked binding is custom
        self.pbSample.clicked.connect(self.setSample)

        self.pbRender = QtWidgets.QPushButton(self.centralwidget)
        self.pbRender.setGeometry(QtCore.QRect(410, 370, 101, 27))
        self.pbRender.setObjectName("pbRender")

        # this clicked binding is custom
        self.pbRender.clicked.connect(self.render)

        self.pbClear = QtWidgets.QPushButton(self.centralwidget)
        self.pbClear.setGeometry(QtCore.QRect(650, 370, 101, 27))
        self.pbClear.setObjectName("pbClear")
        self.pbClear.clicked.connect(self.clearAll)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(820, 380, 111, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 380, 121, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 40, 121, 17))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 965, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionExit)
        self.actionExit.triggered.connect(sys.exit)
        self.menuHelp.addAction(self.actionAbout)
        self.actionAbout.triggered.connect(self.showAboutDialog)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # this form does not use a layout manager, so the window size needs to be set to a fixed geometry
        MainWindow.setFixedSize(MainWindow.size())
        # set window to center screen
        qtRectangle = MainWindow.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        MainWindow.move(qtRectangle.topLeft())
        qtRectangle = MainWindow.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        MainWindow.move(qtRectangle.topLeft())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Template Render"))
        self.pbSample.setText(_translate("MainWindow", "Sample"))
        self.pbRender.setText(_translate("MainWindow", "Render"))
        self.pbClear.setText(_translate("MainWindow", "Clear"))
        self.label.setText(_translate("MainWindow", "MTL Result"))
        self.label_2.setText(_translate("MainWindow", "CLI Content"))
        self.label_3.setText(_translate("MainWindow", "MTL Tempate"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))

    def setSample(self):
        sampleCLI = '''RP/0/RSP0/CPU0:asr9k1#sh int TenGigE0/0/2/0
Sat Dec  8 13:37:02.464 MST
TenGigE0/0/2/0 is up, line protocol is up
  Interface state transitions: 1
  Hardware is TenGigE, address is d46d.503b.6913 (bia d46d.503b.6913)
  Layer 1 Transport Mode is LAN
  Description: SW1_Eth1/37
  Internet address is Unknown
  MTU 9202 bytes, BW 10000000 Kbit (Max: 10000000 Kbit)
     reliability 255/255, txload 0/255, rxload 2/255
  Encapsulation ARPA,
  Full-duplex, 10000Mb/s, LR, link type is force-up
  output flow control is on, input flow control is on
  Carrier delay (up) is 10 msec
  loopback not set,
  Last link flapped 12w0d
  Last input 00:00:00, output 00:00:00
  Last clearing of "show interface" counters never
  5 minute input rate 99801000 bits/sec, 9198 packets/sec
  5 minute output rate 8000 bits/sec, 3 packets/sec
     82764786634 packets input, 106449075723598 bytes, 7709064 total input drops
     3648686 drops for unrecognized upper-level protocol
     Received 18964502 broadcast packets, 82722699591 multicast packets
              0 runts, 0 giants, 0 throttles, 0 parity
     5279 input errors, 4836 CRC, 0 frame, 0 overrun, 0 ignored, 0 abort
     5792319893 packets output, 7864280346019 bytes, 0 total output drops
     Output 4479975 broadcast packets, 5772754062 multicast packets
     0 output errors, 0 underruns, 0 applique, 0 resets
     0 output buffer failures, 0 output buffers swapped out
     1 carrier transitions
'''
        self.teSource.setPlainText(sampleCLI)

        sampleMTL = '''[[fieldbegin='macaddress', method=MID, match=', address is ']]@[[fieldend='macaddress', match='(bia']]
[[fieldbegin='MTU', method=MID, match='MTU ']]@[[fieldend='MTU', match='bytes, BW']]
[[fieldbegin='inputerrors', method=BOL]]@[[fieldend='inputerrors', match=' input errors']]
[[fieldbegin='description', method=EOL, match='Description: ']]@[[fieldend='description', match=' \\n']]
[[fieldbegin='internetaddress', method=EOL, match='Internet address is ']]@[[fieldend='internetaddress', match=' \\n']]
[[fieldbegin='drops', method=BOL]]@[[fieldend='drops', match='drops for unrecognized']]
[[fieldbegin='totaloutputdrops', method=MID, match='bytes, ']]@[[fieldend='totaloutputdrops', match='total output drops']]'''
        self.teTemplate.setPlainText(sampleMTL)

    def clearAll(self):
        # self.ptResult.setPlainText("")
        self.teTemplate.setPlainText("")
        self.teResult.setPlainText("")
        self.teSource.setPlainText("")

    def showAboutDialog(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)

        msg.setText("Welcome to pyqt5 CLI Output and MTL Rendering Tool")
        msg.setWindowTitle("Qt5 Tools")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

        retval = msg.exec_()
        print("value of pressed message box button:", retval)

    def render(self):
        #template = []
        template = self.teTemplate.toPlainText().splitlines()
        pp(template)
        output = str(self.teSource.toPlainText())
        outputlist = output.splitlines()
        #print(str(self.textEdit_2.toPlainText()))
        # QtCore.pyqtRemoveInputHook()
        # pdb.set_trace()
        data = mtl.renderValidator(template, outputlist, "test1")
        # QtCore.pyqtRemoveInputHook()
        # pdb.set_trace()
        datajson = json.dumps(data, indent=2)
        self.teResult.setPlainText(datajson)
        # # pp(data)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    if darkstyle == True:
        # ==== this is NOT generated by pyuic5
        # https://gist.github.com/gph03n1x/7281135
        app.setStyle('Fusion')
        palette = QtGui.QPalette()
        # colors are RBG - http://doc.qt.io/qt-5/qcolor.html
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15, 15, 15))
        palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
        palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
        # Set highlight background to light blue
        palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(65, 105, 225).lighter())
        palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
        app.setPalette(palette)
        # ====== end of custom color palette
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

