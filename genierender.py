# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'genierender.ui'
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
from genie import parsergen


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(956, 717)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.teSource = QtWidgets.QTextEdit(self.centralwidget)
        self.teSource.setGeometry(QtCore.QRect(30, 70, 611, 291))
        self.teSource.setObjectName("teSource")
        self.teSource.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.teSource.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.teSource.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.teTemplate = QtWidgets.QTextEdit(self.centralwidget)
        self.teTemplate.setGeometry(QtCore.QRect(680, 70, 241, 291))
        self.teTemplate.setObjectName("teTemplate")
        self.teResult = QtWidgets.QTextEdit(self.centralwidget)
        self.teResult.setGeometry(QtCore.QRect(30, 410, 901, 231))
        self.teResult.setObjectName("teResult")
        self.pbSample = QtWidgets.QPushButton(self.centralwidget)
        self.pbSample.setGeometry(QtCore.QRect(190, 370, 101, 27))
        self.pbSample.setObjectName("pbSample")
        self.pbSample.clicked.connect(self.showSample)
        self.pbRender = QtWidgets.QPushButton(self.centralwidget)
        self.pbRender.setGeometry(QtCore.QRect(410, 370, 101, 27))
        self.pbRender.setObjectName("pbRender")
        self.pbRender.clicked.connect(self.runGenieParser)
        self.pbClear = QtWidgets.QPushButton(self.centralwidget)
        self.pbClear.setGeometry(QtCore.QRect(650, 370, 101, 27))
        self.pbClear.setObjectName("pbClear")
        self.pbClear.clicked.connect(self.clearAll)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 390, 101, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 50, 101, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(680, 50, 151, 17))
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(860, 40, 61, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(860, 20, 71, 17))
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 956, 22))
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
        self.label.setText(_translate("MainWindow", "Genie Results"))
        self.label_2.setText(_translate("MainWindow", "CLI Content"))
        self.label_3.setText(_translate("MainWindow", "Genie Fields Template"))
        self.lineEdit.setText(_translate("MainWindow", "0"))
        self.label_4.setText(_translate("MainWindow", "Key Field"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))

    def runGenieParser(self):

        content = self.teSource.toPlainText()
        cheaders = self.teTemplate.toPlainText()
        keystring =self.lineEdit.text()
        columnheaders = str(cheaders).split("\n")
        # columnheaders =  ['Device ID', 'Local Intrfce', 'Holdtme', 'Capability', 'Platform', 'Port ID']

        try:
            keys = int(keystring)
            res = parsergen.oper_fill_tabular(device_output=str(content),
                                              table_terminal_pattern=r"^\n",
                                              header_fields=columnheaders,
                                              index=keys)
        except:
            # old python method, still works in Python 3 print('Error:', sys.exc_info()[1])
            print('Error:', sys.exc_info()[1])

        result = res.entries
        resulttxt = json.dumps(result, indent=2)
        self.teResult.setPlainText(resulttxt)

    def showAboutDialog(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)

        msg.setText("Welcome to pyqt5 CLI Output and Genie Parsing Tool")
        msg.setWindowTitle("Qt5 Tools")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        #pop up window here:
        retval = msg.exec_()
        #print("value of pressed message box button:", retval)

    def showSample(self):
        print("sample loading...")
        # pdb.set_trace()
        res = ""
        output = '''IP Interface Status for VRF "default"(1)
Interface            IP Address      Interface Status
Vlan100              172.20.100.2    protocol-up/link-up/admin-up       
Vlan102              172.17.102.2    protocol-up/link-up/admin-up       
Eth1/1               172.20.4.2      protocol-up/link-up/admin-up       
Eth1/5               172.20.3.2      protocol-up/link-up/admin-up       
    '''
        #output = output.replace(" ", "\t")
        sampleheader = "Interface\nIP Address\nInterface Status"
        self.teSource.setPlainText(output)
        self.teTemplate.setPlainText(sampleheader)

    def clearAll(self):
        # self.ptResult.setPlainText("")
        self.teTemplate.setPlainText("")
        self.teResult.setPlainText("")
        self.teSource.setPlainText("")



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

