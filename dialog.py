# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(397, 195)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.formLayoutWidget = QtWidgets.QWidget(Form)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 241))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setHorizontalSpacing(1)
        self.formLayout.setObjectName("formLayout")
        self.inputbox = QgsMapLayerComboBox(self.formLayoutWidget)
        self.inputbox.setProperty("allowEmptyLayer", False)
        self.inputbox.setProperty("showCrs", False)
        self.inputbox.setObjectName("inputbox")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.inputbox)
        self.label_2 = QtWidgets.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.label_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.output = QtWidgets.QLineEdit(self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.output.sizePolicy().hasHeightForWidth())
        self.output.setSizePolicy(sizePolicy)
        self.output.setText("")
        self.output.setObjectName("output")
        self.horizontalLayout_4.addWidget(self.output)
        self.outputb = QtWidgets.QPushButton(self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputb.sizePolicy().hasHeightForWidth())
        self.outputb.setSizePolicy(sizePolicy)
        self.outputb.setMaximumSize(QtCore.QSize(30, 16777215))
        self.outputb.setObjectName("outputb")
        self.horizontalLayout_4.addWidget(self.outputb)
        self.formLayout.setLayout(8, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.label = QtWidgets.QLabel(self.formLayoutWidget)
        self.label.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.label.setObjectName("label")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.label)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(100, -1, -1, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.addout = QtWidgets.QCheckBox(self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addout.sizePolicy().hasHeightForWidth())
        self.addout.setSizePolicy(sizePolicy)
        self.addout.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.addout.setChecked(True)
        self.addout.setObjectName("addout")
        self.horizontalLayout_3.addWidget(self.addout)
        self.formLayout.setLayout(9, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setContentsMargins(150, -1, 0, 5)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.run = QtWidgets.QPushButton(self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(216)
        sizePolicy.setVerticalStretch(40)
        sizePolicy.setHeightForWidth(self.run.sizePolicy().hasHeightForWidth())
        self.run.setSizePolicy(sizePolicy)
        self.run.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.run.setObjectName("run")
        self.horizontalLayout_2.addWidget(self.run)
        self.formLayout.setLayout(10, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.progressBar = QtWidgets.QProgressBar(self.formLayoutWidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.FieldRole, self.progressBar)
        self.label_2.setBuddy(self.label_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Kuwahara Filter"))
        self.label_2.setText(_translate("Form", "Output Raster"))
        self.output.setPlaceholderText(_translate("Form", "<temporary file>"))
        self.outputb.setText(_translate("Form", "..."))
        self.label.setText(_translate("Form", "Input raster"))
        self.addout.setText(_translate("Form", "Add results to project"))
        self.run.setText(_translate("Form", "Run"))

from qgsmaplayercombobox import QgsMapLayerComboBox
