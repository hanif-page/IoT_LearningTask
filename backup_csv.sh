#!/bin/bash

# Load file from the .env file! (this will ignores the commented line and take all the env variables)
export $(grep -v '^#' .env | xargs)

PYMODBUS_CSV_SOURCE=/home/pi/Hanif/IoT_LearningTask/raspi/library/pymodbus/data/pymodbus_data.csv
MINIMALMODBUS_CSV_SOURCE=/home/pi/Hanif/IoT_LearningTask/raspi/library/minimal_modbus/data/minimalmodbus_data.csv
MYMODBUS_CSV_SOURCE=/home/pi/Hanif/IoT_LearningTask/raspi/no_library/data/mymodbus_data.csv
TARGET_FOLDER_PATH="'/home/hanif/Documents/Work/ITB de Labo/raspi_backup'"
NEW_TARGET_FOLDER_NAME="CSVBackup_$(date +%Y-%m-%d_%H-%M-%S)"

/usr/bin/expect<<EOD

spawn sftp $USER@$HOST
expect "password: "
send "$PASSWORD\r"

expect "sftp> "
send "mkdir $TARGET_FOLDER_PATH/$NEW_TARGET_FOLDER_NAME\r"

expect "sftp> "
send "put $PYMODBUS_CSV_SOURCE $TARGET_FOLDER_PATH/$NEW_TARGET_FOLDER_NAME\r"

expect "sftp> "
send "put $MINIMALMODBUS_CSV_SOURCE $TARGET_FOLDER_PATH/$NEW_TARGET_FOLDER_NAME\r"

expect "sftp> "
send "put $MYMODBUS_CSV_SOURCE $TARGET_FOLDER_PATH/$NEW_TARGET_FOLDER_NAME\r"

expect "sftp> "

send "File Backed!\r"

EOD