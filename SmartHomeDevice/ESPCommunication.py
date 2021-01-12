#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Edward J. C. Ashenbert'
__credits__ = ["Edward J. C. Ashenbert"]
__maintainer__ = "Edward J. C. Ashenbert"
__email__ = "nguyenquangbinh803@gmail.com"
__copyright__ = "Copyright 2020"
__status__ = "Working on deploy stage 2"
__version__ = "2020.10.17"

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import re
import serial
import serial.tools.list_ports

from datetime import datetime
from SmartHomeDevice.CommandDescription import *
from UltilitiesAndMacro import *

class ESPCommunication:
    __instance = None

    @staticmethod
    def getInstance():

        if ESPCommunication.__instance == None:
            print("Create new instance")
            return ESPCommunication()

        else:
            return ESPCommunication.__instance

    def __init__(self, serial_port, serial_baudrate):

        if ESPCommunication.__instance != None:
            raise Exception("Thís instance has been created")
        else:
            ESPCommunication.__instance = self
            self.system_state = 0
            self.serial_port = None
            self.serial_baudrate = 115200
            self.serial_connect_status = False

            while not self.serial_port:
                self.diagnostic_logging("Loading esp deivce ...")
                for port in list(serial.tools.list_ports.comports()):
                    print(port.__dict__)
                    res = re.search("Silicon Labs CP210x USB to UART Bridge", port.description)
                    if res:
                        self.serial_port = port.device


            self.diagnostic_logging("Connecting to " + str(self.serial_port) + str(self.serial_baudrate))
            while not self.serial_connect_status:
                try:
                    self.serial = serial.Serial(self.serial_port, self.serial_baudrate, timeout=None)
                    self.system_state += 1
                    self.serial_connect_status = True
                    time.sleep(1)
                except serial.serialutil.SerialException as exp:
                    self.diagnostic_logging("Connect failed due to" + str(exp))

            self.diagnostic_logging("Connected to serial port " + str(self.serial_port))

            self.serial.reset_input_buffer()
            self.serial.reset_output_buffer()
            self.device = []

            # Check binding connection
            device_return_status, device_return_data = self.read_data_from_serial()
            while not device_return_status:
                if device_return_data == LIST_OF_CODE["BINDING_SUCCESS"]:
                    self.diagnostic_logging("Activated connection")


    def define_device(self):
        pass

    def diagnostic_logging(self, message):
        print("[ESPCommunication]", "[" + datetime.now().strftime("%Y%m%d") + "]", "[" + datetime.now().strftime("%H%M%S%f") + "]", message)

    def write_data_to_serial(self, command):
        cmd = str(command)
        try:
            self.serial.write(bytes(cmd, 'utf-8'))
            self.diagnostic_logging(cmd)
            time.sleep(COMMAND_SAMPLING_TIME)

        except serial.SerialException as exp:
            self.diagnostic_logging(str(exp))
            self.serial.close()
            self.diagnostic_logging("Disconnect to serial")
            time.sleep(1)
            try:
                self.serial = serial.Serial(self.serial_port, self.serial_baudrate)
                self.diagnostic_logging("Reconnected to serial")
                time.sleep(1)
                self.serial.write(bytes(cmd, 'utf-8'))
                self.diagnostic_logging(cmd)
                time.sleep(COMMAND_SAMPLING_TIME)
            except serial.SerialException as exp:
                self.diagnostic_logging("Reconnect run into " + str(exp))

    def read_data_from_serial(self):
        device_return_data = ""
        device_return_status = False

        try:
            bytesRead = self.serial.inWaiting()
            device_return_data = self.serial.read(bytesRead).decode("utf-8")
        except serial.SerialException as exp:
            self.diagnostic_logging(str(exp))
            self.serial.close()
            self.diagnostic_logging("Disconnect to serial")
            time.sleep(1)
            try:
                self.serial = serial.Serial(self.serial_port, self.serial_baudrate)
                self.diagnostic_logging("Reconnected to serial")
                time.sleep(1)
                bytesRead = self.serial.inWaiting()
                device_return_data = self.serial.read(bytesRead).decode("utf-8")
            except serial.SerialException as exp:
                self.diagnostic_logging("Reconnect run into " + str(exp))

        if device_return_data == LIST_OF_CODE["CANNOT_FOUND_DEVICE"]:
            device_return_status = False
            device_return_data = ""
        else:
            device_return_status = True
        self.diagnostic_logging(device_return_data)
        return device_return_status, device_return_data



if __name__ == "__main__":
    # ESP_PORT, ESP_BAUDRATE
    esp = ESPCommunication()
    # esp.broadcast_all_device("ON")
    # print(esp.fetch_all_device_info())

    command = {"device_id": "1",
                "device_name": "aklsdmsad",
                "device_command": "ON"
                }
    esp.broadcast_single_device(command)
    time.sleep(0.1)
    command = {"device_id": "1",
               "device_name": "PHONG_KHACH",
               "device_command": "ON "
               }
    esp.broadcast_single_device(command)
    time.sleep(0.1)
    command = {"device_id": "1",
               "device_name": "PHONG_HOP",
               "device_command": "OFF"
               }
    esp.broadcast_single_device(command)
    time.sleep(0.1)
    while True:
        esp.broadcast_single_device(command)
        time.sleep(0.1)

    # esp.broadcast_single_device(command)
    # esp.broadcast_single_device("PHONG_KHACH", "OFF")
    # esp.broadcast_single_device("PHONG_NGU", "ON")


