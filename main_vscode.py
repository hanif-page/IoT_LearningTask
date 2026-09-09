# Multiple pages in one window
# https://forum.qt.io/topic/130564/switching-between-multiple-pages/3
# https://www.tutorialspoint.com/pyqt/pyqt_qstackedwidget.htm

# Very Good
# https://www.patreon.com/spinntv/posts/part-8-modern-ui-51314036
# https://doc.qt.io/qtforpython-6/tutorials/basictutorial/uifiles.html (converting ui to py file)

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from PySide6.QtCore import QCoreApplication, QTimer, Qt
from ui_mainwindow import Ui_MainWindow

from vscode_no_raspi.library.pymodbus.main_usb import PyModbusModule # importing the class!
from vscode_no_raspi.library.minimal_modbus.main_usb import MinimalModbusModule # importing the class!
from vscode_no_raspi.no_library.main_usb import MyModbusModule

# MATPLOTLIB CANVAS
# https://www.pythonguis.com/tutorials/pyside6-plotting-matplotlib/
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure

class MatplotlibCanvas(FigureCanvas):

    def __init__(self, parent=None, width=10, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)

class MainWindow(QMainWindow):
    def __init__(self, modbusModule, modbusClient, baudRate: int):
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
        self.baudRate = baudRate

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Pymodbus")

        # Stacked Pages (default page)
        self.ui.stackedWidget.setCurrentWidget(self.ui.optionDisplay)

        # When monitor_button clicked
        self.ui.monitor_button.clicked.connect(self.runMonitorDisplay)

        self.ui.stopAndSave_button.clicked.connect(self.stopMonitorDisplay)

        # The Data Loop & Delay using QTimer! (explanation: In the IoT Task Notion!!)
        # https://doc.qt.io/qtforpython-6/PySide6/QtCore/QTimer.html
        self.monitorTimer = QTimer()
        self.monitorTimer.setInterval(5000) # 5000ms or 5s delay!
        self.monitorTimer.timeout.connect(self.updateMonitoringData) # when the 5 second ends, call the recurring function inside the connect parameter!

        # When control_button clicked
        self.ui.control_button.clicked.connect(self.runControlDisplay)

        # When Display Time-Base Data clicked
        self.ui.display_time_base_data_button.clicked.connect(self.runTimeBaseDataDisplay)
        self.ui.exit_button_4.clicked.connect(self.stopTimeBaseDataDisplay)

        # When Generate Time-Base Data Button clicked
        # self.ui.generate_data_button.clicked.connect(lambda: print(f"Date: {self.ui.dateInput.date().day()}-{self.ui.dateInput.date().month()}-{self.ui.dateInput.date().year()}"))
        self.ui.generate_data_button.clicked.connect(lambda: self.updateTimeBaseDataDisplay(self.ui.dateInput.date().day(), self.ui.dateInput.date().month(), self.ui.dateInput.date().year()))

        self.show()

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

        # SFTP BACKUP MESSAGE
        self.ui.sftp_connected_msg.setText("")
        # self.ui.sftp_connected_msg.setText("Target Backup Computer Connected! Continuously Backing Up CSV Data Every 1 Minute.")
        # self.ui.sftp_not_connected_msg.setText("")
        self.ui.sftp_not_connected_msg.setText("*The Target Backup Computer Is Not Connected! (Please Click Enable)")


        # hiding the error msg for the port error and library error as default
        # self.ui.port_error_msg.setText("*Error When Accessing Port. Please set the correct Port!")
        # self.ui.library_error_msg.setText("*Error When Using Library. Please use the other Library!")
        self.ui.port_error_msg.setText("")
        self.ui.library_error_msg.setText("")

        # getting the port and library input from the user and call the recurring function
        self.ui.update_settings_button.clicked.connect(self.updatePortAndLibrary)

    def updatePortAndLibrary(self):
        newPort = self.ui.port_input.toPlainText()
        newLibrary = self.ui.library_pick.currentText()

        # closing the previous connection!
        self.modbusModule.closeConnection(self.modbusClient)

        if newLibrary == "Pymodbus":
            # PYMODBUS MODULE
            pymodbus = PyModbusModule(port=newPort, baudRate=self.baudRate, deviceAddress=1)
            pymodbusClient = pymodbus.connectToClient()

            self.modbusModule = pymodbus
            self.modbusClient = pymodbusClient

            self.setWindowTitle("Pymodbus")
        elif newLibrary == "Minimalmodbus":
            # MINIMALMODBUS MODULE
            minimalmodbus = MinimalModbusModule(port=newPort, baudRate=self.baudRate, deviceAddress=1)
            minimalmodbusClient = minimalmodbus.connectToClient()

            self.modbusModule = minimalmodbus
            self.modbusClient = minimalmodbusClient

            self.setWindowTitle("Minimalmodbus")
        elif newLibrary == "Serial (no library)":
            self.setWindowTitle("Mymodbus (Pyserial)")

            # MYMODBUS MODULE (Py Serial)
            mymodbus = MyModbusModule(port=newPort, baudRate=self.baudRate, deviceAddress=1)
            mymodbusClient = mymodbus.connectToClient()   

            self.modbusModule = mymodbus
            self.modbusClient = mymodbusClient 
            
    def runMonitorDisplay(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.monitorDisplay)
        self.ui.update_settings_button.setEnabled(False) # disabling the setting button outside the Option Display!

        self.isMonitoring = True

        # set the first data displayed in the table (before entering the QTimer loop interval)
        self.updateMonitoringData()

        # start the QTimer interval timer! 
        self.monitorTimer.start()
    def stopMonitorDisplay(self):
        self.isMonitoring = False
        self.ui.stackedWidget.setCurrentWidget(self.ui.optionDisplay)
        self.ui.update_settings_button.setEnabled(True) # enabling the setting button in the Option Display!

        # stop the QTimer interval timer! 
        self.monitorTimer.stop()

        print("\nOut from the Monitor Display!\n")
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
        self.ui.update_settings_button.setEnabled(False) # disabling the setting button outside the Option Display!
    def setBaudRate(self, baudRate: int):
        if self.modbusModule.changeBaudRate(self.modbusClient, baudRate):
            print(f"Baud Rate successfully changed to {baudRate}")
            self.isBaudRateControlSuccess = True
            self.baudRate = baudRate

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
            self.ui.update_settings_button.setEnabled(True) # enabling the setting button in the Option Display!
            self.controlTimer.stop()

            self.ui.label_9.setText(QCoreApplication.translate("MainWindow", u"", None))
            self.ui.newBaudRate_value.setText(QCoreApplication.translate("MainWindow", u"", None))

            print("\nOut from the Control Display!\n")
        else:
            self.ui.stackedWidget.setCurrentWidget(self.ui.optionDisplay)
            print("\nOut from the Control Display!\n")

    def runTimeBaseDataDisplay(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.timeBaseDataOptionDisplay)
        self.ui.update_settings_button.setEnabled(False) # disabling the setting button outside the Option Display!
    def filterTimeBaseData(self, dd, mm, yy, listOfData):
        filteredTimeData = []
        filteredTemperatureData = []
        filteredHumidityData = []

        for data in listOfData:
            splittedDate = data["date"].split("-")
            if int(splittedDate[0]) == yy and int(splittedDate[1]) == mm and int(splittedDate[2]) == dd:
                print(data["time"])

                filteredTimeData.append(data["time"])
                filteredTemperatureData.append(data["temperature"])
                filteredHumidityData.append(data["humidity"])

        return filteredTimeData, filteredTemperatureData, filteredHumidityData
    def updateTimeBaseDataDisplay(self, dd, mm, yy):
        print(f"Generate Button Clicked! {dd}-{mm}-{yy}")

        listOfData = self.modbusModule.getListOfData()

        timeData, temperatureData, humidityData = self.filterTimeBaseData(dd, mm, yy, listOfData=listOfData)

        # Generate Time Base Chart
        # NOTE: Try this next https://stackoverflow.com/questions/63785150/displaying-matplotlib-charts-in-groupbox-in-pyqt5 
        sc = MatplotlibCanvas(self, width=5, height=10, dpi=82)

        # NOTE: If we have generated a graph, we can't dynamically change the data directly, we need to EXIT and reopen the program to refresh it... 
        # Possible solution (later, try to debug): https://www.geeksforgeeks.org/python/dynamically-updating-plot-in-matplotlib/
        sc.axes.clear()

        # https://stackoverflow.com/questions/14762181/adding-a-y-axis-label-to-secondary-y-axis-in-matplotlib
        ax1 = sc.axes
        ax2 = sc.axes.twinx()

        ax1.axes.plot(timeData, temperatureData, "b")
        ax2.axes.plot(timeData, humidityData, "g")

        ax1.set_ylabel("Temperature (°C)", color="b")
        ax2.set_ylabel("Humidity (%RH)", color="g")
        ax1.set_xlabel("Time")

        for tick in ax1.axes.get_xticklabels():
            tick.set_rotation(45)
        # ax1.axes.set_xticklabels(ax1.get_xticks(), rotation=45)

        matplotlibLayout = QVBoxLayout()
        matplotlibLayout.addWidget(sc)
        matplotlibLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.ui.plotData_container.setFixedHeight(490)
        self.ui.plotData_container.setLayout(matplotlibLayout)

    def stopTimeBaseDataDisplay(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.optionDisplay)
        self.ui.update_settings_button.setEnabled(True) # enabling the setting button in the Option Display!

        print("\nOut from the Time-Base Data Display!\n")

def main(port: str, baudRate: int) -> None:
    # PYMODBUS MODULE (DEFAULT)
    pymodbus = PyModbusModule(port=port, baudRate=baudRate, deviceAddress=1)
    pymodbusClient = pymodbus.connectToClient()

    app = QApplication(sys.argv)

    window = MainWindow(modbusModule=pymodbus, modbusClient=pymodbusClient, baudRate=baudRate)    

    window.show()

    # Red Exit Button
    window.ui.exit_button.clicked.connect(app.quit)    

    sys.exit(app.exec())

if __name__ == "__main__":
    # parameter is the default Port and BaudRate
    main(port="/dev/ttyUSB0", baudRate=9600)