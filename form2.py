# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created: Mon Feb 04 21:25:16 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import kuw_filter
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_form1(object):
    def setupUi(self, form1):
        form1.setObjectName(_fromUtf8("form1"))
        form1.resize(400, 260)
        form1.setFocusPolicy(QtCore.Qt.TabFocus)
        form1.setWindowTitle(_fromUtf8("Kuwahara filter"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/qgis.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        form1.setWindowIcon(icon)
        self.label = QtGui.QLabel(form1)
        self.label.setGeometry(QtCore.QRect(21, 12, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setToolTip(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))
        self.outputb = QtGui.QPushButton(form1)
        self.outputb.setGeometry(QtCore.QRect(320, 49, 31, 23))
        self.outputb.setObjectName(_fromUtf8("outputb"))
        self.label_2 = QtGui.QLabel(form1)
        self.label_2.setGeometry(QtCore.QRect(22, 51, 101, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setToolTip(_fromUtf8(""))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.progressBar = QtGui.QProgressBar(form1)
        self.progressBar.setGeometry(QtCore.QRect(19, 227, 361, 23))
        self.progressBar.setProperty(_fromUtf8("value"), 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.label_3 = QtGui.QLabel(form1)
        self.label_3.setGeometry(QtCore.QRect(22, 90, 131, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(form1)
        self.label_4.setGeometry(QtCore.QRect(21, 127, 181, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.run = QtGui.QPushButton(form1)
        self.run.setGeometry(QtCore.QRect(139, 187, 101, 23))
        self.run.setObjectName(_fromUtf8("run"))
        self.input = QtGui.QComboBox(form1)
        self.input.setGeometry(QtCore.QRect(141, 12, 170, 22))
        self.input.setObjectName(_fromUtf8("input"))
        self.output = QtGui.QLineEdit(form1)
        self.output.setGeometry(QtCore.QRect(149, 47, 160, 28))
        self.output.setObjectName(_fromUtf8("output"))
        self.refb = QtGui.QLineEdit(form1)
        self.refb.setGeometry(QtCore.QRect(149, 84, 160, 28))
        self.refb.setObjectName(_fromUtf8("refb"))
        self.mem = QtGui.QLineEdit(form1)
        self.mem.setGeometry(QtCore.QRect(208, 122, 101, 28))
        self.mem.setObjectName(_fromUtf8("mem"))
        self.addout = QtGui.QCheckBox(form1)
        self.addout.setGeometry(QtCore.QRect(100, 160, 171, 17))
        self.addout.setChecked(True)
        self.addout.setObjectName(_fromUtf8("addout"))
        self.path = QtGui.QLineEdit(form1)
        self.path.setGeometry(QtCore.QRect(280, 180, 113, 20))
        self.path.setObjectName(_fromUtf8("path"))
        self.path.setVisible(False)
        self.retranslateUi(form1)
        QtCore.QMetaObject.connectSlotsByName(form1)
        self.setFixedSize(self.width(), self.height())

    def retranslateUi(self, form1):
        self.label.setText(QtGui.QApplication.translate("form1", "Raster de entrada", None, QtGui.QApplication.UnicodeUTF8))
        self.outputb.setText(QtGui.QApplication.translate("form1", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("form1", "Raster de saida", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setToolTip(QtGui.QApplication.translate("form1", "Banda de referência, sobre a qual serão calculadas as variâncias para escolher a subjanela a ser utilizada.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("form1", "Banda de referência", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setToolTip(QtGui.QApplication.translate("form1", "Máxima carga de memória a ser utilizada (o valor é aproximado já que o algoritmo apenas escolhe o número de linhas a serem lidas por vez).", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("form1", "Máximo uso da memoria (MB)", None, QtGui.QApplication.UnicodeUTF8))
        self.run.setText(QtGui.QApplication.translate("form1", "Run!", None, QtGui.QApplication.UnicodeUTF8))
        self.output.setText(QtGui.QApplication.translate("form1", "<temporario>", None, QtGui.QApplication.UnicodeUTF8))
        self.refb.setToolTip(QtGui.QApplication.translate("form1", "Banda de referência, sobre a qual serão calculadas as variâncias para escolher a subjanela a ser utilizada.", None, QtGui.QApplication.UnicodeUTF8))
        self.refb.setText(QtGui.QApplication.translate("form1", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.mem.setToolTip(QtGui.QApplication.translate("form1", "Máxima carga de memória a ser utilizada (o valor é aproximado já que o algoritmo apenas escolhe o número de linhas a serem lidas por vez).", None, QtGui.QApplication.UnicodeUTF8))
        self.mem.setText(QtGui.QApplication.translate("form1", "100", None, QtGui.QApplication.UnicodeUTF8))
        self.addout.setText(QtGui.QApplication.translate("form1", "Adicionar resultados ao projeto", None, QtGui.QApplication.UnicodeUTF8))

import resources
