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
import textfsm
from textfsm import TextFSMTemplateError
import os, sys
from pprint import pprint as pp

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
        self.pbRender.clicked.connect(self.runParser)

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
        self.label.setText(_translate("MainWindow", "TFSM Result"))
        self.label_2.setText(_translate("MainWindow", "CLI Content"))
        self.label_3.setText(_translate("MainWindow", "TextFSM Tempate"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))

    def runParser(self):
        templatefile = str(uuid.uuid4()) + ".textfsm"
        print("parsing using ... \n" + templatefile)
        tfsmcontent = self.teTemplate.toPlainText()
        clicontent = self.teSource.toPlainText()
        filewpath = "./" + templatefile
        fh = open(filewpath, 'w')
        fh.write(tfsmcontent)
        fh.close()
        print(filewpath)

        filehandle = open(filewpath, "r")

        # parser takes a filehandle on an open file containing template
        try:
            re_table = textfsm.TextFSM(filehandle)
            fsm_results = re_table.ParseText(str(clicontent))
        except TextFSMTemplateError:
            print("TextFSM Template Parsing Failure : " + str(sys.exc_info()[1]))
            errmsg = QMessageBox()
            errmsg.move(MainWindow.rect().center())
            errmsg.about(errmsg,'TextFSM message',str(sys.exc_info()[1]))
        except:
            # old python method, still works in Python 3 print('Error:', sys.exc_info()[1])
            print('Error:', sys.exc_info()[1])


        filehandle.close()
        if os.path.exists(filewpath):
            print("removing file: " + filewpath)
            os.remove(filewpath)
        else:
            print("problem deleting tmp file... The file does not exist")

        resultDictionary = {}
        resultDictionary["Content"] = []
        for row in fsm_results:
            print(row)
            temprecord = {}
            # walk the row (list of strings) - use header to key the dict
            for position in range(0, len(re_table.header)):
                # print(re_table.header[position])
                temprecord[re_table.header[position]] = row[position]
            resultDictionary["Content"].append(temprecord)
        jsonresult = json.dumps(resultDictionary, indent=2)
        print(jsonresult)
        self.teResult.setPlainText(jsonresult)

    def setSample(self):
        sampleCLI = '''Ethernet1/0 is up, line protocol is up 
Hardware is AmdP2, address is ca01.3f99.001c (bia ca01.3f99.001c)
Description: To Cloud Carrier
Internet address is 172.17.1.1/24
MTU 1500 bytes, BW 10000 Kbit/sec, DLY 1000 usec, 
 reliability 255/255, txload 1/255, rxload 1/255
Encapsulation ARPA, loopback not set
Keepalive set (10 sec)
ARP type: ARPA, ARP Timeout 04:00:00
Last input 00:00:00, output 00:00:07, output hang never
Last clearing of "show interface" counters never
Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
Queueing strategy: fifo
Output queue: 0/40 (size/max)
5 minute input rate 0 bits/sec, 0 packets/sec
5 minute output rate 0 bits/sec, 0 packets/sec
 30 packets input, 4026 bytes, 0 no buffer
 Received 27 broadcasts (13 IP multicasts)
 0 runts, 0 giants, 0 throttles 
 0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
 0 input packets with dribble condition detected
 51 packets output, 5299 bytes, 0 underruns
 0 output errors, 0 collisions, 1 interface resets
 0 unknown protocol drops
 0 babbles, 0 late collision, 0 deferred
 0 lost carrier, 0 no carrier
 0 output buffer failures, 0 output buffers swapped out
'''
        self.teSource.setPlainText(sampleCLI)

        samppleTFSM = '''Value Required INTERFACE (\S+)
Value LINK_STATUS (.+?)
Value PROTOCOL_STATUS (.+?)
Value HARDWARE_TYPE ([\w ]+)
Value ADDRESS ([a-fA-F0-9]{4}\.[a-fA-F0-9]{4}\.[a-fA-F0-9]{4})
Value BIA ([a-fA-F0-9]{4}\.[a-fA-F0-9]{4}\.[a-fA-F0-9]{4})
Value DESCRIPTION (.+?)
Value IP_ADDRESS (\d+\.\d+\.\d+\.\d+\/\d+)
Value MTU (\d+)
Value DUPLEX (([Ff]ull|[Aa]uto|[Hh]alf|[Aa]-).*?)
Value SPEED (.*?)
Value BANDWIDTH (\d+\s+\w+)
Value DELAY (\d+\s+\S+)
Value ENCAPSULATION (.+?)
Value LAST_INPUT (.+?)
Value LAST_OUTPUT (.+?)
Value LAST_OUTPUT_HANG (.+?)
Value QUEUE_STRATEGY (.+)
Value INPUT_RATE (\d+)
Value OUTPUT_RATE (\d+)
Value INPUT_PACKETS (\d+)
Value OUTPUT_PACKETS (\d+)
Value INPUT_ERRORS (\d+)
Value OUTPUT_ERRORS (\d+)

Start
  ^\S+\s+is\s+.+?,\s+line\s+protocol.*$$ -> Continue.Record
  ^${INTERFACE}\s+is\s+${LINK_STATUS},\s+line\s+protocol\s+is\s+${PROTOCOL_STATUS}\s*$$
  ^\s+Hardware\s+is\s+${HARDWARE_TYPE} -> Continue
  ^.+address\s+is\s+${ADDRESS}\s+\(bia\s+${BIA}\)\s*$$
  ^\s+Description:\s+${DESCRIPTION}\s*$$
  ^\s+Internet\s+address\s+is\s+${IP_ADDRESS}\s*$$
  ^\s+MTU\s+${MTU}.*BW\s+${BANDWIDTH}.*DLY\s+${DELAY},\s*$$
  ^\s+Encapsulation\s+${ENCAPSULATION},.+$$
  ^\s+Last\s+input\s+${LAST_INPUT},\s+output\s+${LAST_OUTPUT},\s+output\s+hang\s+${LAST_OUTPUT_HANG}\s*$$
  ^\s+Queueing\s+strategy:\s+${QUEUE_STRATEGY}\s*$$
  ^\s+${DUPLEX},\s+${SPEED},.+$$
  ^.*input\s+rate\s+${INPUT_RATE}.+$$
  ^.*output\s+rate\s+${OUTPUT_RATE}.+$$
  ^\s+${INPUT_PACKETS}\s+packets\s+input,\s+\d+\s+bytes,\s+\d+\s+no\s+buffer\s*$$
  ^\s+${INPUT_ERRORS}\s+input\s+errors,\s+\d+\s+CRC,\s+\d+\s+frame,\s+\d+\s+overrun,\s+\d+\s+ignored\s*$$
  ^\s+${OUTPUT_PACKETS}\s+packets\s+output,\s+\d+\s+bytes,\s+\d+\s+underruns\s*$$
  ^\s+${OUTPUT_ERRORS}\s+output\s+errors,\s+\d+\s+collisions,\s+\d+\s+interface\s+resets\s*$$'''
        self.teTemplate.setPlainText(samppleTFSM)

    def clearAll(self):
        # self.ptResult.setPlainText("")
        self.teTemplate.setPlainText("")
        self.teResult.setPlainText("")
        self.teSource.setPlainText("")

    def showAboutDialog(self):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Information)

        msg.setText("Welcome to pyqt5 CLI Output and TextFSM Rendering Tool")
        # msg.setInformativeText("This is additional information")
        msg.setWindowTitle("Qt5 Tools")
        # msg.setDetailedText("The details are as follows:")
        # msg.setStandardButtons(QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        # msg.buttonClicked.

        retval = msg.exec_()
        print("value of pressed message box button:", retval)


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

