# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHeaderView,
    QLabel, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QStackedWidget, QStatusBar,
    QTableWidget, QTableWidgetItem, QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(801, 684)
        MainWindow.setStyleSheet(u"background-color: white;")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 781, 61))
        self.groupBox.setStyleSheet(u"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 5px;\n"
"border-color: black")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 10, 761, 41))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(16)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet(u"color: black;\n"
"border-color: white;")
        self.label.setAlignment(Qt.AlignCenter)
        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(10, 440, 781, 181))
        self.groupBox_4.setStyleSheet(u"color: black;\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 5px;\n"
"border-color: black")
        self.port = QLabel(self.groupBox_4)
        self.port.setObjectName(u"port")
        self.port.setGeometry(QRect(10, 50, 51, 21))
        font1 = QFont()
        font1.setPointSize(13)
        font1.setBold(True)
        self.port.setFont(font1)
        self.port.setStyleSheet(u"border-color: white")
        self.sensor = QLabel(self.groupBox_4)
        self.sensor.setObjectName(u"sensor")
        self.sensor.setGeometry(QRect(10, 10, 81, 21))
        self.sensor.setFont(font1)
        self.sensor.setStyleSheet(u"border-color: white")
        self.library = QLabel(self.groupBox_4)
        self.library.setObjectName(u"library")
        self.library.setGeometry(QRect(10, 100, 71, 21))
        self.library.setFont(font1)
        self.library.setStyleSheet(u"border-color: white")
        self.sensor_name = QLabel(self.groupBox_4)
        self.sensor_name.setObjectName(u"sensor_name")
        self.sensor_name.setGeometry(QRect(90, 10, 661, 21))
        font2 = QFont()
        font2.setPointSize(13)
        font2.setBold(True)
        font2.setItalic(False)
        self.sensor_name.setFont(font2)
        self.sensor_name.setStyleSheet(u"border-color: white")
        self.library_pick = QComboBox(self.groupBox_4)
        self.library_pick.addItem("")
        self.library_pick.addItem("")
        self.library_pick.addItem("")
        self.library_pick.setObjectName(u"library_pick")
        self.library_pick.setGeometry(QRect(90, 90, 171, 41))
        font3 = QFont()
        font3.setPointSize(13)
        self.library_pick.setFont(font3)
        self.port_input = QTextEdit(self.groupBox_4)
        self.port_input.setObjectName(u"port_input")
        self.port_input.setGeometry(QRect(90, 40, 171, 41))
        self.update_settings_button = QPushButton(self.groupBox_4)
        self.update_settings_button.setObjectName(u"update_settings_button")
        self.update_settings_button.setGeometry(QRect(10, 140, 251, 31))
        self.update_settings_button.setFont(font1)
        self.update_settings_button.setStyleSheet(u"color: white;\n"
"background-color: green;\n"
"border-radius: 5px")
        self.port_error_msg = QLabel(self.groupBox_4)
        self.port_error_msg.setObjectName(u"port_error_msg")
        self.port_error_msg.setGeometry(QRect(270, 60, 501, 21))
        font4 = QFont()
        font4.setPointSize(12)
        font4.setBold(False)
        font4.setItalic(True)
        self.port_error_msg.setFont(font4)
        self.port_error_msg.setStyleSheet(u"border-color: white;\n"
"color: red")
        self.library_error_msg = QLabel(self.groupBox_4)
        self.library_error_msg.setObjectName(u"library_error_msg")
        self.library_error_msg.setGeometry(QRect(270, 110, 501, 21))
        self.library_error_msg.setFont(font4)
        self.library_error_msg.setStyleSheet(u"border-color: white;\n"
"color: red")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setGeometry(QRect(10, 80, 781, 351))
        self.stackedWidget.setStyleSheet(u"color: black;")
        self.optionDisplay = QWidget()
        self.optionDisplay.setObjectName(u"optionDisplay")
        self.option_container = QGroupBox(self.optionDisplay)
        self.option_container.setObjectName(u"option_container")
        self.option_container.setGeometry(QRect(0, 0, 781, 351))
        self.option_container.setStyleSheet(u"color: black;\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 5px;\n"
"border-color: black")
        self.label_2 = QLabel(self.option_container)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 30, 751, 21))
        font5 = QFont()
        font5.setFamilies([u"MS Shell Dlg 2"])
        font5.setPointSize(14)
        font5.setBold(True)
        self.label_2.setFont(font5)
        self.label_2.setStyleSheet(u"color: black;\n"
"border-color: white")
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.option_layout = QGroupBox(self.option_container)
        self.option_layout.setObjectName(u"option_layout")
        self.option_layout.setGeometry(QRect(10, 60, 761, 281))
        self.option_layout.setStyleSheet(u"border-color: white")
        self.monitor_button = QPushButton(self.option_layout)
        self.monitor_button.setObjectName(u"monitor_button")
        self.monitor_button.setGeometry(QRect(10, 30, 361, 41))
        font6 = QFont()
        font6.setPointSize(12)
        self.monitor_button.setFont(font6)
        self.monitor_button.setStyleSheet(u"background-color: rgb(221, 221, 255);\n"
"color: black;\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 5px;\n"
"border-color: rgb(85, 0, 255);")
        self.exit_button = QPushButton(self.option_layout)
        self.exit_button.setObjectName(u"exit_button")
        self.exit_button.setGeometry(QRect(650, 240, 101, 31))
        font7 = QFont()
        font7.setPointSize(12)
        font7.setBold(True)
        self.exit_button.setFont(font7)
        self.exit_button.setStyleSheet(u"background-color: red;\n"
"color: white;\n"
"border-radius: 5px")
        self.control_button = QPushButton(self.option_layout)
        self.control_button.setObjectName(u"control_button")
        self.control_button.setGeometry(QRect(390, 30, 361, 41))
        self.control_button.setFont(font6)
        self.control_button.setStyleSheet(u"background-color: rgb(221, 221, 255);\n"
"color: black;\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 5px;\n"
"border-color: rgb(85, 0, 255);")
        self.stackedWidget.addWidget(self.optionDisplay)
        self.monitorDisplay = QWidget()
        self.monitorDisplay.setObjectName(u"monitorDisplay")
        self.monitorDisplay.setStyleSheet(u"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 5px;\n"
"border-color: black")
        self.monitor_data_timestamp = QLabel(self.monitorDisplay)
        self.monitor_data_timestamp.setObjectName(u"monitor_data_timestamp")
        self.monitor_data_timestamp.setGeometry(QRect(10, 10, 751, 31))
        self.monitor_data_timestamp.setFont(font5)
        self.monitor_data_timestamp.setStyleSheet(u"border-color: white")
        self.monitor_data_timestamp.setAlignment(Qt.AlignCenter)
        self.stopAndSave_button = QPushButton(self.monitorDisplay)
        self.stopAndSave_button.setObjectName(u"stopAndSave_button")
        self.stopAndSave_button.setGeometry(QRect(520, 310, 251, 31))
        font8 = QFont()
        font8.setPointSize(11)
        font8.setBold(True)
        self.stopAndSave_button.setFont(font8)
        self.stopAndSave_button.setStyleSheet(u"background-color: red;\n"
"color: white;\n"
"border-radius: 5px")
        self.monitor_data_layout = QGroupBox(self.monitorDisplay)
        self.monitor_data_layout.setObjectName(u"monitor_data_layout")
        self.monitor_data_layout.setGeometry(QRect(10, 50, 761, 251))
        self.monitor_data_layout.setStyleSheet(u"border-color: white")
        self.data_table = QTableWidget(self.monitor_data_layout)
        if (self.data_table.columnCount() < 1):
            self.data_table.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.data_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        if (self.data_table.rowCount() < 6):
            self.data_table.setRowCount(6)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.data_table.setVerticalHeaderItem(0, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.data_table.setVerticalHeaderItem(1, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.data_table.setVerticalHeaderItem(2, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.data_table.setVerticalHeaderItem(3, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.data_table.setVerticalHeaderItem(4, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.data_table.setVerticalHeaderItem(5, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.data_table.setItem(0, 0, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.data_table.setItem(1, 0, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.data_table.setItem(2, 0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.data_table.setItem(3, 0, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.data_table.setItem(4, 0, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.data_table.setItem(5, 0, __qtablewidgetitem12)
        self.data_table.setObjectName(u"data_table")
        self.data_table.setGeometry(QRect(10, 30, 741, 211))
        self.data_table.setStyleSheet(u"")
        self.stackedWidget.addWidget(self.monitorDisplay)
        self.controlDisplay = QWidget()
        self.controlDisplay.setObjectName(u"controlDisplay")
        self.controlDisplay.setStyleSheet(u"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 5px;\n"
"border-color: black")
        self.label_7 = QLabel(self.controlDisplay)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(10, 10, 751, 31))
        self.label_7.setFont(font5)
        self.label_7.setStyleSheet(u"border-color: white")
        self.label_7.setAlignment(Qt.AlignCenter)
        self.control_data_layout = QGroupBox(self.controlDisplay)
        self.control_data_layout.setObjectName(u"control_data_layout")
        self.control_data_layout.setGeometry(QRect(10, 60, 761, 281))
        self.label_8 = QLabel(self.control_data_layout)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(10, 30, 731, 31))
        font9 = QFont()
        font9.setFamilies([u"MS Shell Dlg 2"])
        font9.setPointSize(12)
        font9.setBold(True)
        self.label_8.setFont(font9)
        self.label_8.setStyleSheet(u"border-color: white")
        self.set9600_button = QPushButton(self.control_data_layout)
        self.set9600_button.setObjectName(u"set9600_button")
        self.set9600_button.setGeometry(QRect(20, 70, 221, 41))
        self.set9600_button.setFont(font6)
        self.set9600_button.setStyleSheet(u"QPushButton {\n"
"background-color: rgb(221, 221, 255);\n"
"color: black;\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 5px;\n"
"border-color: rgb(85, 0, 255);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"opacity: 50%;\n"
"}")
        self.set14400_button = QPushButton(self.control_data_layout)
        self.set14400_button.setObjectName(u"set14400_button")
        self.set14400_button.setGeometry(QRect(270, 70, 221, 41))
        self.set14400_button.setFont(font6)
        self.set14400_button.setStyleSheet(u"QPushButton {\n"
"background-color: rgb(221, 221, 255);\n"
"color: black;\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 5px;\n"
"border-color: rgb(85, 0, 255);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"opacity: 50%;\n"
"}")
        self.set19200_button = QPushButton(self.control_data_layout)
        self.set19200_button.setObjectName(u"set19200_button")
        self.set19200_button.setGeometry(QRect(520, 70, 221, 41))
        self.set19200_button.setFont(font6)
        self.set19200_button.setStyleSheet(u"QPushButton {\n"
"background-color: rgb(221, 221, 255);\n"
"color: black;\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 5px;\n"
"border-color: rgb(85, 0, 255);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"opacity: 50%;\n"
"}")
        self.baudRate_updated_text = QGroupBox(self.control_data_layout)
        self.baudRate_updated_text.setObjectName(u"baudRate_updated_text")
        self.baudRate_updated_text.setGeometry(QRect(10, 230, 731, 41))
        self.baudRate_updated_text.setStyleSheet(u"border-color: white")
        self.label_9 = QLabel(self.baudRate_updated_text)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(10, 0, 241, 31))
        self.label_9.setFont(font9)
        self.label_9.setStyleSheet(u"border-color: white; color: red")
        self.newBaudRate_value = QLabel(self.baudRate_updated_text)
        self.newBaudRate_value.setObjectName(u"newBaudRate_value")
        self.newBaudRate_value.setGeometry(QRect(240, 0, 191, 31))
        self.newBaudRate_value.setFont(font9)
        self.newBaudRate_value.setStyleSheet(u"border-color: white; color: red")
        self.stackedWidget.addWidget(self.controlDisplay)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 801, 24))
        self.menuDev = QMenu(self.menubar)
        self.menuDev.setObjectName(u"menuDev")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuDev.menuAction())

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"IoT Modbus Program", None))
        self.groupBox_4.setTitle("")
        self.port.setText(QCoreApplication.translate("MainWindow", u"Port:", None))
        self.sensor.setText(QCoreApplication.translate("MainWindow", u"Sensor:", None))
        self.library.setText(QCoreApplication.translate("MainWindow", u"Library:", None))
        self.sensor_name.setText(QCoreApplication.translate("MainWindow", u"XY-MD02", None))
        self.library_pick.setItemText(0, QCoreApplication.translate("MainWindow", u"Pymodbus", None))
        self.library_pick.setItemText(1, QCoreApplication.translate("MainWindow", u"Minimalmodbus", None))
        self.library_pick.setItemText(2, QCoreApplication.translate("MainWindow", u"Serial (no library)", None))

        self.port_input.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Ubuntu Sans'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">/dev/ttyUSB0</p></body></html>", None))
        self.update_settings_button.setText(QCoreApplication.translate("MainWindow", u"Update Settings", None))
        self.port_error_msg.setText(QCoreApplication.translate("MainWindow", u"*Error When Accessing Port. Please set the correct Port!", None))
        self.library_error_msg.setText(QCoreApplication.translate("MainWindow", u"*Error When Using Library. Please use the other Library!", None))
        self.option_container.setTitle("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Please Select One:", None))
        self.option_layout.setTitle("")
        self.monitor_button.setText(QCoreApplication.translate("MainWindow", u"Monitor", None))
        self.exit_button.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.control_button.setText(QCoreApplication.translate("MainWindow", u"Control", None))
        self.monitor_data_timestamp.setText(QCoreApplication.translate("MainWindow", u"MONITOR DATA (%Y-%m-%d %H:%M:%S)", None))
        self.stopAndSave_button.setText(QCoreApplication.translate("MainWindow", u"Stop Monitoring and Save Data", None))
        self.monitor_data_layout.setTitle("")
        ___qtablewidgetitem = self.data_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Value", None));
        ___qtablewidgetitem1 = self.data_table.verticalHeaderItem(0)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Temperature (\u00b0C)", None));
        ___qtablewidgetitem2 = self.data_table.verticalHeaderItem(1)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Humidity (%RH)", None));
        ___qtablewidgetitem3 = self.data_table.verticalHeaderItem(2)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Device Address", None));
        ___qtablewidgetitem4 = self.data_table.verticalHeaderItem(3)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Baud Rate", None));
        ___qtablewidgetitem5 = self.data_table.verticalHeaderItem(4)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Temperature Correction (Raw Data)", None));
        ___qtablewidgetitem6 = self.data_table.verticalHeaderItem(5)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Humidity Correction (Raw Data)", None));

        __sortingEnabled = self.data_table.isSortingEnabled()
        self.data_table.setSortingEnabled(False)
        ___qtablewidgetitem7 = self.data_table.item(0, 0)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"24", None));
        ___qtablewidgetitem8 = self.data_table.item(1, 0)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"48", None));
        ___qtablewidgetitem9 = self.data_table.item(2, 0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"0", None));
        ___qtablewidgetitem10 = self.data_table.item(3, 0)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"9600", None));
        ___qtablewidgetitem11 = self.data_table.item(4, 0)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"0", None));
        ___qtablewidgetitem12 = self.data_table.item(5, 0)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"0", None));
        self.data_table.setSortingEnabled(__sortingEnabled)

        self.label_7.setText(QCoreApplication.translate("MainWindow", u"CONTROL DATA", None))
        self.control_data_layout.setTitle("")
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Please Select the New Baud Rate Option:", None))
        self.set9600_button.setText(QCoreApplication.translate("MainWindow", u"9600", None))
        self.set14400_button.setText(QCoreApplication.translate("MainWindow", u"14400", None))
        self.set19200_button.setText(QCoreApplication.translate("MainWindow", u"19200", None))
        self.baudRate_updated_text.setTitle("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"*Baud Rate Changed To: ", None))
        self.newBaudRate_value.setText(QCoreApplication.translate("MainWindow", u"9600", None))
        self.menuDev.setTitle(QCoreApplication.translate("MainWindow", u"Dev", None))
    # retranslateUi

