# Multiple pages in one window
# https://forum.qt.io/topic/130564/switching-between-multiple-pages/3
# https://www.tutorialspoint.com/pyqt/pyqt_qstackedwidget.htm

# Very Good
# https://www.patreon.com/spinntv/posts/part-8-modern-ui-51314036
# https://doc.qt.io/qtforpython-6/tutorials/basictutorial/uifiles.html (converting ui to py file)

import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QCoreApplication
from ui_mainwindow import Ui_MainWindow

from datetime import datetime
import time

from raspi.library.pymodbus.main_usb import PyModbusModule # importing the class!
# from raspi.library.minimal_modbus.main_usb 
# from raspi.no_library import main_usb as pyserial # but this still won't work because I haven't develop it!

class MainWindow(QMainWindow):
    def __init__(self, modbusClient):
        super(MainWindow, self).__init__()

        """
        This modbusClient could be Pymodbus, Minimalmodbus, or Pyserial

        Requirements: We need to set Pymodbus, Minimalmodbus, and Pyserial with the same function under it. Let:
        - connectToClient()
        - changeBaudRate(client, newBaudRate)
        - getMonitoredData(client) 
        """
        self.modbusClient = modbusClient

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Stacked Pages (default page)
        self.ui.stackedWidget.setCurrentWidget(self.ui.optionDisplay)

        # When monitor_button clicked
        self.ui.monitor_button.clicked.connect(self.runMonitorDisplay)

        # When control_button clicked
        self.ui.control_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.controlDisplay))

        # later, create an additional function to run the process
        self.ui.set9600_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.optionDisplay))
        self.ui.set14400_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.optionDisplay))
        self.ui.set19200_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.optionDisplay))

        # Displaying the Changed Baud Rate only after one of the button clicked! (Control Display)
        # self.ui.label_9.setText(QCoreApplication.translate("MainWindow", u"*Baud Rate Changed To: ", None))
        # self.ui.newBaudRate_value.setText(QCoreApplication.translate("MainWindow", u"9600", None))
        self.ui.label_9.setText(QCoreApplication.translate("MainWindow", u"", None))
        self.ui.newBaudRate_value.setText(QCoreApplication.translate("MainWindow", u"", None))

        # getting the port and library input from the user!
        self.ui.update_settings_button.clicked.connect(lambda: print(f"Port: {self.ui.port_input.toPlainText()}\nLibrary: {self.ui.library_pick.currentText()}"))

    def runMonitorDisplay(self):
        # changing the stacked pages to the Monitor Page
        self.ui.stackedWidget.setCurrentWidget(self.ui.monitorDisplay)

        self.isMonitoring = True

        self.ui.stopAndSave_button.clicked.connect(self.stopMonitorDisplay)

        # Run the loop to continuously change the data!
        while self.isMonitoring:
            print("Capturing Data...")
            ... # the monitoring and save logic

            time.sleep(5) # 5 second interval

        """
        CURRENT BIG PROBLEM: I haven't figure this bug out, but, the main problem is when I click the monitor button, the Pages won't changed, but the while loop runs!
        """

    def stopMonitorDisplay(self):
        self.isMonitoring = False
        self.ui.stackedWidget.setCurrentWidget(self.ui.optionDisplay)
        print("Out from the Monitor Display!")


    def runControlDisplay(self):
        ...

# class ModbusClient:
#     def __init__(self, modbusClientModule, clientType: int = 0):
#         """
#         modbusClientModule

#         clientType
#             0: Pymodbus (default)
#             1: Minimalmodbus
#             2: Pyserial
#         """
#         self.modbusClientModule = modbusClientModule
#         self.clientType = clientType

#     def 
        

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

    window = MainWindow(pymodbusClient)    

    # strDate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # this is doable, but I haven't check if this is OK or NOT OK in OOP concept! 
    # window.ui.monitor_data_timestamp.setText(QCoreApplication.translate("MainWindow", f"MONITOR DATA ({strDate})", None))

    window.show()

    # This Works!
    window.ui.exit_button.clicked.connect(app.quit)    

    sys.exit(app.exec())