from __future__ import absolute_import
from builtins import object
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created: Tue Feb 05 22:32:50 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from qgis.PyQt import QtCore, QtGui
from qgis.PyQt.QtWidgets import QLabel, QPushButton, QWidget, QProgressBar, QLineEdit, QCheckBox, QApplication
from qgis.gui import QgsMapLayerComboBox
from . import kuw_filter as kw
from sys import exit
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_form1(object):
    def setupUi(self, form1):
        form1.setObjectName(_fromUtf8("form1"))
        form1.resize(400, 253)
        form1.setFocusPolicy(QtCore.Qt.TabFocus)
        form1.setWindowTitle(_fromUtf8("Kuwahara filter"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/qgis.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        form1.setWindowIcon(icon)
        self.label = QLabel(form1)
        self.label.setGeometry(QtCore.QRect(21, 10, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setToolTip(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))
        self.outputb = QPushButton(form1)
        self.outputb.setGeometry(QtCore.QRect(320, 47, 31, 23))
        self.outputb.setObjectName(_fromUtf8("outputb"))
        self.label_2 = QLabel(form1)
        self.label_2.setGeometry(QtCore.QRect(22, 49, 101, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setToolTip(_fromUtf8(""))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.progressBar = QProgressBar(form1)
        self.progressBar.setGeometry(QtCore.QRect(19, 220, 361, 23))
        self.progressBar.setProperty(_fromUtf8("value"), 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.label_3 = QLabel(form1)
        self.label_3.setGeometry(QtCore.QRect(22, 88, 131, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QLabel(form1)
        self.label_4.setGeometry(QtCore.QRect(21, 125, 181, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.run = QPushButton(form1)
        self.run.setGeometry(QtCore.QRect(139, 185, 101, 23))
        self.run.setObjectName(_fromUtf8("run"))
        self.inputbox = QgsMapLayerComboBox(form1)
        self.inputbox.setGeometry(QtCore.QRect(141, 10, 170, 22))
        self.inputbox.setObjectName(_fromUtf8("input"))
        self.output = QLineEdit(form1)
        self.output.setGeometry(QtCore.QRect(149, 45, 160, 28))
        self.output.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.output.setObjectName(_fromUtf8("output"))
        self.refb = QLineEdit(form1)
        self.refb.setGeometry(QtCore.QRect(149, 82, 160, 28))
        self.refb.setObjectName(_fromUtf8("refb"))
        self.mem = QLineEdit(form1)
        self.mem.setGeometry(QtCore.QRect(208, 120, 101, 28))
        self.mem.setObjectName(_fromUtf8("mem"))
        self.addout = QCheckBox(form1)
        self.addout.setGeometry(QtCore.QRect(100, 158, 171, 17))
        self.addout.setChecked(True)
        self.addout.setObjectName(_fromUtf8("checkBox"))
        self.inputb = QPushButton(form1)
        self.inputb.setGeometry(QtCore.QRect(320, 10, 31, 23))
        self.inputb.setObjectName(_fromUtf8("inputb"))
        self.retranslateUi(form1)
        self.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowCloseButtonHint))
        QtCore.QMetaObject.connectSlotsByName(form1)
    def retranslateUi(self, form1):
        self.label.setText(QtCore.QCoreApplication.translate("form1", "Input raster"))
        self.outputb.setText("...")
        self.label_2.setText(QApplication.translate("form1", "Output raster"))
        self.label_3.setToolTip(QApplication.translate("form1", "Reference band from which variances will be calculated to choose subwindow mean."))
        self.label_3.setText(QApplication.translate("form1", "Reference band"))
        self.label_4.setToolTip(QApplication.translate("form1", "Maximum memory usage in megabytes (it is an approximated value, since algorithm will only choose how many lines will be read at once)."))
        self.label_4.setText(QApplication.translate("form1", "Max memory usage (MB)"))
        self.run.setText(QApplication.translate("form1", "Run"))
        self.output.setPlaceholderText(QApplication.translate("form1", "<temporary file>"))
        self.refb.setToolTip(QApplication.translate("form1", "Reference band from which variances will be calculated to choose subwindow mean."))
        self.refb.setText("1")
        self.mem.setToolTip(QApplication.translate("form1", "Maximum memory usage in MeB (it is an approximated value, since algorithm will only choose how many lines will be read at once)."))
        self.mem.setText("100")
        self.addout.setText(QApplication.translate("form1", "Add results to project"))
        self.inputb.setText("...")
from . import resources

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form1 = QWidget()
    ui = Ui_form1()
    ui.setupUi(form1)
    form1.show()
    sys.exit(app.exec_())

