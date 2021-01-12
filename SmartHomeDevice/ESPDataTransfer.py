__author__ = 'Edward J. C. Ashenbert'
__credits__ = ["Edward J. C. Ashenbert"]
__maintainer__ = "Edward J. C. Ashenbert"
__email__ = "nguyenquangbinh803@gmail.com"
__copyright__ = "Copyright 2020"
__status__ = "Working on demo stage 2, develop the entire local server for all raspberry"
__version__ = "1.0.1"

import sys
import os
import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from SmartHomeDevice.ESPCommunication import ESPCommunication
from SmartHomeDevice.CommandDescription import *


class ESPDataTransfer(ESPCommunication):
    def __init__(self, trasnfer_port, transfer_baudrate):
        super().__init__(trasnfer_port, transfer_baudrate)

    def broadcast_all_device(self, device_command, return_type="json"):

        device_info = dict.fromkeys(LIST_OF_KEYS)

        self.write_data_to_serial(BROADCAST_ALL_DEVICE + DELIMITER + device_command + EOF)
        time.sleep(1)

        device_return_data = self.read_data_from_serial()

        if return_type == "json":
            return device_info
        else:
            return device_return_data

    def broadcast_single_device(self, control_command, return_type="json"):

        device_info = dict.fromkeys(LIST_OF_KEYS)
        device_return_data = ""
        device_name = control_command["device_name"]
        device_id = control_command["device_id"]
        device_command = control_command["device_command"]

        try:
            self.write_data_to_serial(BROADCAST_SINGLE_DEVICE + DELIMITER + device_name + DELIMITER + device_command + EOF)
            time.sleep(0.2)

            device_return_status, device_return_data = self.read_data_from_serial()

        except Exception as exp:
            print("Overall exception ", str(exp))

        if return_type == "json":
            return device_info
        else:
            return device_return_data

    def get_all_device_description(self):
        self.write_data_to_serial(GET_ALL_DEVICE_DESCRIPTION + EOF)
        bytesRead = self.serial.inWaiting()
        self.device.append(self.serial.read(bytesRead))
        return True

    def fetch_all_device_info(self, return_type="json"):
        # <message>,<device_id>,<device_name>,<device_type>,<device_status>;
        device_info = dict.fromkeys(LIST_OF_KEYS)
        device_return_data_compile = []
        return_message = dict.fromkeys(["message", "devices"])
        list_of_device_info = []
        device_return_data = ""
        try:
            self.write_data_to_serial(FETCH_ALL_DEVICE_STATUS + EOF)
            time.sleep(3)
            print("[esp_serial_logging] " + str(datetime.now().time()) + SPACE + "Fetching all devices ")

            bytesRead = self.serial.inWaiting()
            device_return_data = self.serial.read(bytesRead).decode("utf-8")
        except:
            pass

        # Compile device return data
        for device in device_return_data.split(";"):
            device_return_data_compile.append(device.split(","))
        print(device_return_data_compile)
        for device in device_return_data_compile[:-1]:
            device_info = dict.fromkeys(LIST_OF_KEYS)
            device_info["message"] = device[0]
            device_info["device_id"] = device[1]
            device_info["device_name"] = device[2]
            device_info["device_type"] = device[3]
            device_info["device_status"] = device[4]
            list_of_device_info.append(device_info)

        if device_return_data:
            return_message["message"] = SUCCESS_MESSSAGE
            return_message["devices"] = list_of_device_info
        else:
            return_message["message"] = FAILURE_MESSSAGE
            return_message["devices"] = list_of_device_info

        if return_type == "json":
            return return_message
        else:
            return device_return_data

    def fetch_single_device_info(self, device_name, return_type="json"):

        device_info = dict.fromkeys(LIST_OF_KEYS)
        device_return_data = "Nothing"
        try:
            self.write_data_to_serial(FETCH_SINGLE_DEVICE_STATUS + DELIMITER + device_name + EOF)
            time.sleep(1)
            print("[esp_serial_logging] " + str(datetime.now().time()) + SPACE + "Fetching signle device ", device_name)
            bytesRead = self.serial.inWaiting()
            device_return_data = self.serial.read(bytesRead)
        except:
            pass

        device_info["name"] = device_name
        device_info["status"] = device_return_data

        if return_type == "json":
            return device_info
        else:
            return device_return_data
