# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'jytool.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
darkstyle = True
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDesktopWidget, QMessageBox
import json
import uuid
import os, sys, traceback
from pprint import pprint as pp
import jinja2
import yaml

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(956, 717)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.teJinja = QtWidgets.QTextEdit(self.centralwidget)
        self.teJinja.setGeometry(QtCore.QRect(30, 70, 411, 291))
        self.teJinja.setObjectName("teJinja")
        self.teYaml = QtWidgets.QTextEdit(self.centralwidget)
        self.teYaml.setGeometry(QtCore.QRect(480, 70, 441, 291))
        self.teYaml.setObjectName("teYaml")
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
        self.pbRender.clicked.connect(self.renderJinja2)
        self.pbClear = QtWidgets.QPushButton(self.centralwidget)
        self.pbClear.setGeometry(QtCore.QRect(650, 370, 101, 27))
        self.pbClear.setObjectName("pbClear")
        self.pbClear.clicked.connect(self.clearAll)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 40, 231, 17))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(490, 40, 161, 17))
        self.label_2.setObjectName("label_2")
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Jinja Template Render"))
        self.pbSample.setText(_translate("MainWindow", "Sample"))
        self.pbRender.setText(_translate("MainWindow", "Render"))
        self.pbClear.setText(_translate("MainWindow", "Clear"))
        self.label.setText(_translate("MainWindow", "Jinja Config Template"))
        self.label_2.setText(_translate("MainWindow", "YAML data"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))

    def clearAll(self):
        # self.ptResult.setPlainText("")
        self.teJinja.setPlainText("")
        self.teYaml.setPlainText("")
        self.teResult.setPlainText("")

    def showAboutDialog(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)

        msg.setText("Welcome to pyqt5 CLI Jinja and Yaml Rendering Tool\nhttp://jinja.pocoo.org/")
        msg.setWindowTitle("Qt5 Tools")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

        retval = msg.exec_()
        print("value of pressed message box button:", retval)

    def showSample(self):
        print("sample loading...")
        # pdb.set_trace()

        samplejinja = """hostname {{ name }}

    interface Loopback0
      ip address 10.0.0.{{ id }} 255.255.255.255

    {% for vlan, name in vlans.items() %}
    vlan {{ vlan }}
      name {{ name }}
    {% endfor %}

    router ospf 1
      router-id 10.0.0.{{ id }}
      auto-cost reference-bandwidth 10000
    {% for networkareas in ospf%}
      network {{ networkareas.network }} area {{ networkareas.area }}
    {% endfor %}
    """
        sampleyaml = """id: 1
name: R1
vlans:
  100: Managment
  200: Realtime
  300: Server
ospf:
  -  network: 172.20.1.0 0.0.0.255
     area: 0
  -  network: 172.20.0.0 0.0.255.255
     area: 1
"""
        self.teJinja.setPlainText(samplejinja)
        self.teYaml.setPlainText(sampleyaml)

    def renderJinja2(self):

        jinjatxt = str(self.teJinja.toPlainText()).strip()
        yamltxt = str(self.teYaml.toPlainText()).strip()


        try:
            template = jinja2.Template(jinjatxt)
            # get yaml data and convert to dictionary for jinja to consume
            ydata = yaml.load(yamltxt)
            result = template.render(ydata)
            self.teResult.setPlainText(result)
        except Exception:
            print('Error rendering yaml/jinja to text:', sys.exc_info()[1])
            self.ptResult.setPlainText('Error rendering yaml/jinja to text')
            print('Trace info:')
            print(traceback.format_exc())


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

