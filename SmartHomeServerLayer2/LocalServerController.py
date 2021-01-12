__author__ = 'Edward J. C. Ashenbert'
__credits__ = ["Edward J. C. Ashenbert"]
__maintainer__ = "Edward J. C. Ashenbert"
__email__ = "nguyenquangbinh803@gmail.com"
__copyright__ = "Copyright 2020"
__status__ = "Working on demo in Can Tho city"
__version__ = "1.1.0"

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import threading
import uuid
from datetime import datetime
import requests

class LocalServerController:

    def __init__(self):
        self.diagnostic_logging("Start local server controller")
        self.available_layer1_server = []
        self.list_of_layer1_server_identification = []
        self.scan_layer_1_server()

    def diagnostic_logging(self, message):
        print("[LocalServerController]", "[" + datetime.now().strftime("%Y%m%d_%H%M%S%f") + "]", message)

    def scan_layer_1_server(self):
        self.diagnostic_logging("Start scan procedure")
        # threading.Thread(target=self.scan_layer_1_server_procedure).start()
        index = 0
        for i in range(1, 2):
            for j in range(255):
                self.layer1_server_identification = dict.fromkeys(["server_name", "ip_address", "devices"])
                try:
                    ip_address = "http://192.168." + str(i) + "." + str(j) + ":5000/"
                    res = requests.get(ip_address, timeout=0.01)
                    if res.ok:
                        self.layer1_server_identification["ip_address"] = ip_address
                        self.layer1_server_identification["server_name"] = str(uuid.uuid1())
                        self.list_of_layer1_server_identification.append(self.layer1_server_identification)
                        index += 1
                except Exception as exp:
                    self.diagnostic_logging(str(exp))

        self.diagnostic_logging("Done scanning layer 1 server")
        self.diagnostic_logging(self.list_of_layer1_server_identification)


    def scan_layer_1_server_procedure(self):
        index = 0
        for i in range(1, 2):
            for j in range(255):
                self.layer1_server_identification = dict.fromkeys(["server_name", "ip_address", "devices"])
                try:
                    ip_address = "http://192.168." + str(i) + "." + str(j) + ":5000/"
                    res = requests.get(ip_address, timeout=0.01)
                    if res.ok:
                        self.layer1_server_identification["ip_address"] = ip_address
                        self.layer1_server_identification["server_name"] = str(uuid.uuid1())
                        self.list_of_layer1_server_identification.append(self.layer1_server_identification)
                        index += 1
                except Exception as exp:
                    self.diagnostic_logging(str(exp))

        self.diagnostic_logging("Done scanning layer 1 server")
        self.diagnostic_logging(self.list_of_layer1_server_identification)

    def scan_all_device_of_layer1_server(self):
        self.diagnostic_logging("Start scan all device in each layer 1 server")
        for index, layer1_server in enumerate(self.list_of_layer1_server_identification):
            request_message = "get_devices_info"
            response = requests.get(layer1_server["ip_address"] + request_message, timeout=1)
            if response.ok:
                self.diagnostic_logging("Query succeed")
                self.list_of_layer1_server_identification[index]["devices"] = response.json()["devices"]
                # self.diagnostic_logging(self.list_of_layer1_server_identification)
            else:
                self.diagnostic_logging("Query failed")
        self.diagnostic_logging("Finished scan layer 1 server devices")

    def send_ultimate_command(self, command):
        for ip_address in self.layer1_server_identification["ip_address"]:
            requests.get(ip_address, timeout=0.01)


import time


def request_1(local_server_controller):
    while True:
        local_server_controller.scan_all_device_of_layer1_server()
        print(threading.current_thread().ident)
        time.sleep(0.002)


def request_2(local_server_controller):
    while True:
        local_server_controller.scan_all_device_of_layer1_server()
        print(threading.current_thread().ident)
        # time.sleep(0.002)


def request_3(local_server_controller):
    while True:
        local_server_controller.scan_all_device_of_layer1_server()
        print(threading.current_thread().ident)
        # time.sleep(0.002)

if __name__ == "__main__":
    local_server_controller = LocalServerController()

    threading.Thread(target=request_1, args=[local_server_controller, ]).start()
    threading.Thread(target=request_2, args=[local_server_controller, ]).start()
    threading.Thread(target=request_3, args=[local_server_controller, ]).start()
