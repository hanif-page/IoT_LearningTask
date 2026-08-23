import csv

# Good source
# https://www.geeksforgeeks.org/python/writing-csv-files-in-python/

class SensorData:
    def __init__(self, filePathRelativeToDriver):
        self.filePathRelativeToDriver = filePathRelativeToDriver
        self.arrOfDicts = []

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

    def createData(
            self,
            date: str,
            time: str,
            temperature: float,
            humidity: float,
            deviceAddress: int,
            baudRate: int,
            temperatureCorrection: float,
            humidityCorrection: float
    ) -> dict:
        newDict = dict(
            date=date,
            time=time,
            temperature=temperature,
            humidity=humidity,
            deviceAddress=deviceAddress,
            baudRate=baudRate,
            temperatureCorrection=temperatureCorrection,
            humidityCorrection=humidityCorrection
        )

        return newDict

    def addData(self, dict) -> dict:
        # process of adding the new dictionary object to the self.arrOfDicts

        try:
            self.arrOfDicts.append(dict)

            return self.arrOfDicts[-1] # return the added dictionary!

        except Exception as e:
            print(f"Error when adding dictionary: {e}")
            return {}

    def saveDataToCsv(self):
        # process of converting the self.arrOfDicts into CSV File with the file name of self.fileName!

        fileName = f"{self.arrOfDicts[0]['date']}_{self.arrOfDicts[0]['time']}_sensorData.csv"

        # print(fileName)

        try:
            with open(f"{self.filePathRelativeToDriver}/{fileName}", "w", newline="") as csvfile:
                fieldNames = [
                    "date",
                    "time",
                    "temperature",
                    "humidity",
                    "deviceAddress",
                    "baudRate",
                    "temperatureCorrection",
                    "humidityCorrection"
                ]

                writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
                writer.writeheader()
                writer.writerows(self.arrOfDicts)

            print(f"Data saved at {self.filePathRelativeToDriver}/{fileName}\n")

        except Exception as e:
            print(f"Error: {e}")

    def saveDataToBigCSV(self, libraryname: str):
        fileName = f"{libraryname}_data.csv"

        try:
            with open(f"{self.filePathRelativeToDriver}/{fileName}", "a", newline="") as csvfile:
                fieldNames = [
                    "date",
                    "time",
                    "temperature",
                    "humidity",
                    "deviceAddress",
                    "baudRate",
                    "temperatureCorrection",
                    "humidityCorrection"
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
                writer.writerows(self.arrOfDicts)
            print(f"[CSV] Data saved at {self.filePathRelativeToDriver}/{fileName}\n")

        except Exception as e:
            print(f"Error: {e}")