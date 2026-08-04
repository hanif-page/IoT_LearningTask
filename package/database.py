import mysql.connector

# Great Source
# https://stackoverflow.com/questions/37232649/will-creating-an-sql-table-that-already-exists-overwrite-it
# https://youtu.be/91iNR0eG8kE?si=vZClaJ8TD-w8VuDG

# Notes: Belum Pake ORM! Next --> Better pake ORM! (like peewee)

class MySQLData:
    def __init__(self, databaseName, tableName):
        self.databaseName = databaseName
        self.tableName = tableName
        self.isConnected = False

    def connectToMySQL(self):
        """
        Return the db of the connected MySQL
        """
        try:
            self.mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database=self.databaseName
            )

            # problem: to type the mysql -u root -p in the terminal, it needs a sudo

            # sudo usage strategy:
            # ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password USING PASSWORD('your-password');
            # FLUSH PRIVILEGES;

            """
            CSV File Structure
            [
                {
                    "date"
                    "time"
                    "temperature"
                    "humidity"
                    "deviceAddress"
                    "baudRate"
                    "temperatureCorrection"
                    "humidityCorrection"
                },
                {...},
                {...},
                ...,
                {...last item}
            ]
            """

            self.mydb.cursor().execute(f"CREATE TABLE IF NOT EXISTS {self.tableName} (date VARCHAR(50), time VARCHAR(50), temperature float, humidity float, deviceAddress int, baudRate int, temperatureCorrection float, humidityCorrection float, {self.tableName}_ID int PRIMARY KEY AUTO_INCREMENT)")

            self.mydb.commit()

            self.isConnected = True

            # return self.mydb
            return True
        except Exception as e:
            print(f"Error: {e}")

            return False

    def getConnectionStatus(self):
        return self.isConnected

    def addData(self,
        date: str,
        time: str,
        temperature: float,
        humidity: float,
        deviceAddress: int,
        baudRate: int,
        temperatureCorrection: float,
        humidityCorrection: float   
    ):
        if self.isConnected:
            try:
                self.mydb.cursor().execute(f"INSERT INTO {self.tableName} (date, time, temperature, humidity, deviceAddress, baudRate, temperatureCorrection, humidityCorrection) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (date, time, temperature, humidity, deviceAddress, baudRate, temperatureCorrection, humidityCorrection))

                self.mydb.commit()

                return True

            except Exception as e:
                print(f"Error: {e}")

                return False

    def getDataList(self):
        # this is Mandatory! We need to define the cursor function into a variable that might needs to be called later! (with the same .cursor() call)
        mycursor = self.mydb.cursor(dictionary=True) # dictionary=True making the cursor output into a dictionary, not tuple

        mycursor.execute(f"SELECT * FROM {self.tableName}")

        dataList = []

        # return mycursor
        for x in mycursor:
            dataList.append(x)

        return dataList


    def printTableContent(self):

        for data in self.getDataList():
            print(data)

    def closeConnection(self):
        try:
            self.mydb.close()

            return True
        except Exception as e:
            print(f"Error: {e}")

            return False

# testing ground and double check for the processed data
if __name__ == "__main__":
    databaseName = "iot_task"
    tableName = "pymodbus_data"

    MySQLSensorData = MySQLData(databaseName=databaseName, tableName=tableName)

    # _date = "2026-08-01"
    # _time = "12-29-10"
    # _temperature = 27.4
    # _humidity = 38.4
    # _deviceAddress = 1
    # _baudRate = 9600
    # _temperatureCorrection = 0
    # _humidityCorrection = 0

    if MySQLSensorData.connectToMySQL():
        # if MySQLSensorData.addData(
        #     date=_date,
        #     time=_time,
        #     temperature=_temperature,
        #     humidity=_humidity,
        #     deviceAddress=_deviceAddress,
        #     baudRate=_baudRate,
        #     temperatureCorrection=_temperatureCorrection,
        #     humidityCorrection=_humidityCorrection
        # ):
        #     print("Data successfully added!")

        #     MySQLSensorData.printTableContent()   

        #     if MySQLSensorData.closeConnection():
        #         print("Successfully Close Connection!")

        MySQLSensorData.printTableContent()