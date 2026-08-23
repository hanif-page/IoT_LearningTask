# Multiple pages in one window
# https://forum.qt.io/topic/130564/switching-between-multiple-pages/3
# https://www.tutorialspoint.com/pyqt/pyqt_qstackedwidget.htm

# Very Good
# https://www.patreon.com/spinntv/posts/part-8-modern-ui-51314036
# https://doc.qt.io/qtforpython-6/tutorials/basictutorial/uifiles.html (converting ui to py file)

import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QCoreApplication, QTimer
from ui_mainwindow import Ui_MainWindow


from raspi.library.pymodbus.main_usb import PyModbusModule # importing the class!
# from raspi.library.minimal_modbus.main_usb 
# from raspi.no_library import main_usb as pyserial # but this still won't work because I haven't develop it!

class MainWindow(QMainWindow):
    def __init__(self, modbusModule, modbusClient):
        super(MainWindow, self).__init__()

        """
        This modbusModule could be Pymodbus, Minimalmodbus, or Pyserial

        Requirements: We need to set Pymodbus, Minimalmodbus, and Pyserial with the same function under it. Let:
        - connectToClient()
        - changeBaudRate(client, newBaudRate)
        - getMonitoredData(client) 
        """
        self.modbusModule = modbusModule
        self.modbusClient = modbusClient
        self.isMonitoring = False
        self.isBaudRateControlSuccess = False

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Stacked Pages (default page)
        self.ui.stackedWidget.setCurrentWidget(self.ui.optionDisplay)

        # When monitor_button clicked
        self.ui.monitor_button.clicked.connect(self.runMonitorDisplay)

        self.ui.stopAndSave_button.clicked.connect(self.stopMonitorDisplay)

        # The Data Loop & Delay using QTimer! (explanation: In the IoT Task Notion!!)
        # https://doc.qt.io/qtforpython-6/PySide6/QtCore/QTimer.html
        self.monitorTimer = QTimer()
        self.monitorTimer.setInterval(5000) # 5000ms or 5s delay!
        self.monitorTimer.timeout.connect(self.stopControlDisplay) # when the 5 second ends, call the recurring function inside the connect parameter!

        # When control_button clicked
        self.ui.control_button.clicked.connect(self.runControlDisplay)

        # The Delay after one of the baud rate button is clicked
        self.controlTimer = QTimer()
        self.controlTimer.setInterval(3000) # 3s delay!
        self.controlTimer.timeout.connect(self.stopControlDisplay)

        # later, create an additional function to run the process
        self.ui.set9600_button.clicked.connect(lambda: self.setBaudRate(baudRate=9600))
        self.ui.set14400_button.clicked.connect(lambda: self.setBaudRate(baudRate=14400))
        self.ui.set19200_button.clicked.connect(lambda: self.setBaudRate(baudRate=19200))

        # Displaying the Changed Baud Rate only after one of the button clicked! (Control Display)
        # In default, it is set to none because we don't want to show the text at first!
        self.ui.label_9.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.ui.newBaudRate_value.setText(QCoreApplication.translate("MainWindow", u"", None))

        # getting the port and library input from the user!
        self.ui.update_settings_button.clicked.connect(lambda: print(f"Port: {self.ui.port_input.toPlainText()}\nLibrary: {self.ui.library_pick.currentText()}"))

    def runMonitorDisplay(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.monitorDisplay)

        self.isMonitoring = True

        # set the first data displayed in the table (before entering the QTimer loop interval)
        self.updateMonitoringData()

        # start the QTimer interval timer! 
        self.monitorTimer.start()
    def stopMonitorDisplay(self):
        self.isMonitoring = False
        self.ui.stackedWidget.setCurrentWidget(self.ui.optionDisplay)

        # stop the QTimer interval timer! 
        self.monitorTimer.stop()

        print("Out from the Monitor Display!")
    def updateMonitoringData(self):
        try:
            # Get Data
            data = self.modbusModule.getMonitoredData(self.modbusClient)
        
            # change the Monitor Data date and time
            self.ui.monitor_data_timestamp.setText(QCoreApplication.translate("MainWindow", f"MONITOR DATA ({data['date']} {data['time']})", None))

            # Change/Update the table value data
            """
                dictionary template: dict(
                    date=date,
                    time=time,
                    temperature=temperature
                    humidity=humidity,
                    deviceAddress=deviceAddress,
                    baudRate=baudRate,
                    temperatureCorrection=temperatureCorrection,
                    humidityCorrection=humidityCorrection
                )
            """
            self.ui.data_table.item(0, 0).setText(f"{data['temperature']}")
            self.ui.data_table.item(1, 0).setText(f"{data['humidity']}")
            self.ui.data_table.item(2, 0).setText(f"{data['deviceAddress']}")
            self.ui.data_table.item(3, 0).setText(f"{data['baudRate']}")
            self.ui.data_table.item(4, 0).setText(f"{data['temperatureCorrection']}")
            self.ui.data_table.item(5, 0).setText(f"{data['humidityCorrection']}")
        except Exception as e:
            print(f"Error when updating data: {e}")

    def runControlDisplay(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.controlDisplay)
    def setBaudRate(self, baudRate: int):
        if self.modbusModule.changeBaudRate(self.modbusClient, baudRate):
            print(f"Baud Rate successfully changed to {baudRate}")
            self.isBaudRateControlSuccess = True

            self.ui.label_9.setText(QCoreApplication.translate("MainWindow", u"*Baud Rate Changed To:", None))
            self.ui.newBaudRate_value.setText(QCoreApplication.translate("MainWindow", f"{baudRate}", None))

            self.controlTimer.start()
        else:
            print(f"Baud Rate failed to be changed!")
            self.isBaudRateControlSuccess = False
    def stopControlDisplay(self):
        if self.isBaudRateControlSuccess:
            self.isBaudRateControlSuccess = False
            self.ui.stackedWidget.setCurrentWidget(self.ui.optionDisplay)
            self.controlTimer.stop()

            self.ui.label_9.setText(QCoreApplication.translate("MainWindow", u"", None))
            self.ui.newBaudRate_value.setText(QCoreApplication.translate("MainWindow", u"", None))

            print("Out from the Control Display!")
        else:
            self.ui.stackedWidget.setCurrentWidget(self.ui.optionDisplay)
            print("Out from the Control Display!")

if __name__ == "__main__":
    # DEFAULT VALUE
    defaultPort = "/dev/ttyUSB0"
    defaultBaudRate = 9600

    # DEFAULT MODBUS MODULE
    pymodbus = PyModbusModule(port=defaultPort, baudRate=defaultBaudRate)
    pymodbusClient = pymodbus.connectToClient()

    # OTHER MODBUS MODULE
    ...

    app = QApplication(sys.argv)

    window = MainWindow(pymodbus, pymodbusClient)    

    window.show()

    # This Works!
    window.ui.exit_button.clicked.connect(app.quit)    

    sys.exit(app.exec())