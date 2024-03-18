# Form implementation generated from reading ui file 'management_ui.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(750, 500)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(750, 500))
        Form.setMaximumSize(QtCore.QSize(750, 500))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("pictures/wehere_icon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet("background-color: qlineargradient(spread:pad, x1:0.489, y1:1, x2:0.494, y2:0, stop:0 rgba(71, 71, 71, 255), stop:1 rgba(255, 255, 255, 255));")
        self.pushButton_mam_exit = QtWidgets.QPushButton(parent=Form)
        self.pushButton_mam_exit.setGeometry(QtCore.QRect(10, 430, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        self.pushButton_mam_exit.setFont(font)
        self.pushButton_mam_exit.setStyleSheet("QPushButton{\n"
"    border-radius : 15px;\n"
"    background-color : rgb(25, 200, 200);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(20, 135, 135);\n"
" border: 2px solid rgb(162, 0, 0);\n"
"}")
        self.pushButton_mam_exit.setObjectName("pushButton_mam_exit")
        self.label_2 = QtWidgets.QLabel(parent=Form)
        self.label_2.setGeometry(QtCore.QRect(200, 32, 261, 101))
        self.label_2.setStyleSheet("\n"
"background-color: rgba(0, 0, 0,0%);")
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("pictures/wehere_logo.ico"))
        self.label_2.setObjectName("label_2")
        self.pushButton_mam_send_mail = QtWidgets.QPushButton(parent=Form)
        self.pushButton_mam_send_mail.setGeometry(QtCore.QRect(10, 270, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        self.pushButton_mam_send_mail.setFont(font)
        self.pushButton_mam_send_mail.setStyleSheet("QPushButton{\n"
"    border-radius : 15px;\n"
"    background-color : rgb(25, 200, 200);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(20, 135, 135);\n"
" border: 2px solid rgb(162, 0, 0);\n"
"}")
        self.pushButton_mam_send_mail.setObjectName("pushButton_mam_send_mail")
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 191, 171))
        self.label.setStyleSheet("background-color: rgba(0, 0, 0,0%);")
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("pictures/main_admin.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(parent=Form)
        self.label_3.setGeometry(QtCore.QRect(460, 60, 251, 41))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(26)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("background-color: rgba(0, 0, 0,0%);\n"
"color: rgb(71, 84, 88);")
        self.label_3.setObjectName("label_3")
        self.tableWidget = QtWidgets.QTableWidget(parent=Form)
        self.tableWidget.setGeometry(QtCore.QRect(200, 190, 521, 271))
        self.tableWidget.setStyleSheet("background-color: rgba(0, 0, 0,0%);")
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignTop)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(130)
        self.pushButton_back_menu = QtWidgets.QPushButton(parent=Form)
        self.pushButton_back_menu.setGeometry(QtCore.QRect(10, 350, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        self.pushButton_back_menu.setFont(font)
        self.pushButton_back_menu.setStyleSheet("QPushButton{\n"
"    border-radius : 15px;\n"
"    background-color : rgb(25, 200, 200);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(20, 135, 135);\n"
" border: 2px solid rgb(162, 0, 0);\n"
"}")
        self.pushButton_back_menu.setObjectName("pushButton_back_menu")
        self.label_4 = QtWidgets.QLabel(parent=Form)
        self.label_4.setGeometry(QtCore.QRect(410, 110, 121, 41))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(26)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("background-color: rgba(0, 0, 0,0%);\n"
"color: rgb(71, 84, 88);")
        self.label_4.setObjectName("label_4")
        self.pushButton_mam_event_control = QtWidgets.QPushButton(parent=Form)
        self.pushButton_mam_event_control.setGeometry(QtCore.QRect(10, 190, 171, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(True)
        self.pushButton_mam_event_control.setFont(font)
        self.pushButton_mam_event_control.setStyleSheet("QPushButton{\n"
"    border-radius : 15px;\n"
"    background-color : rgb(25, 200, 200);\n"
"    color: rgb(255, 255, 255);\n"
"}\n"
"QPushButton:hover{\n"
"    background-color: rgb(20, 135, 135);\n"
" border: 2px solid rgb(162, 0, 0);\n"
"}")
        self.pushButton_mam_event_control.setObjectName("pushButton_mam_event_control")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.pushButton_mam_event_control, self.pushButton_mam_send_mail)
        Form.setTabOrder(self.pushButton_mam_send_mail, self.pushButton_back_menu)
        Form.setTabOrder(self.pushButton_back_menu, self.tableWidget)
        Form.setTabOrder(self.tableWidget, self.pushButton_mam_exit)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "MAIN ADMIN MENU"))
        self.pushButton_mam_exit.setText(_translate("Form", "Exit"))
        self.pushButton_mam_send_mail.setText(_translate("Form", "Send Mail"))
        self.label_3.setText(_translate("Form", "MAIN ADMIN"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Event Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Start Time"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Participant Mail"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Organizer Mail"))
        self.pushButton_back_menu.setText(_translate("Form", "Back Menu"))
        self.label_4.setText(_translate("Form", "MENU"))
        self.pushButton_mam_event_control.setText(_translate("Form", "Event Control"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
