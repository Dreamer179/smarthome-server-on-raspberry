__author__ = 'Edward J. C. Ashenbert'
__credits__ = ["Edward J. C. Ashenbert"]
__maintainer__ = "Edward J. C. Ashenbert"
__email__ = "nguyenquangbinh803@gmail.com"
__copyright__ = "Copyright 2020"
__status__ = "Working on product version 1"
__version__ = "1.0.1"

from flask import jsonify

from SmartHomeDevice.ESPCommunication import ESPCommunication
from UltilitiesAndMacro import *


class FlaskController:

    def __init__(self):
        self.esp_communication = ESPCommunication(ESP_PORT, ESP_BAUDRATE)
        self.previous_state = False

    def handle_single_device_status(self, device_name):
        # Not use yet
        status = self.esp_communication.fetch_single_device_info(device_name)
        return jsonify(status)

    def handle_all_device_status(self):
        # status = self.esp_communication.fetch_all_device_info()
        # print("Status", status)
        status = {"message": "success",
                 "devices": [{'device_id': "1", 'device_name': 'PHONG_KHACH', 'device_type': 'ONOFF',
                              'device_status': 'OFF'},
                             {'device_id': "2", 'device_name': 'PHONG_NGU', 'device_type': 'COLOR',
                              'device_status': 'WHITE'},
                             {'device_id': "3", 'device_name': 'PHONG_VE_SINH', 'device_type': 'ONOFF',
                              'device_status': 'OFF'},
                             {'device_id': "4", 'device_name': 'DEN_TUONG', 'device_type': 'MULTI_COLOR',
                              'device_status': '#000000'}
                             ]
                 }
        return jsonify(status)

    def handle_control_all_device(self, control_command):
        # Not use yet
        device_command = control_command["device_command"]
        status = self.esp_communication.broadcast_all_device(device_command)
        return jsonify(status)

    def handle_control_curtain(self, control_command):
        # Not use yet
        device_command = control_command["device_command"]
        status = self.esp_communication.broadcast_all_device(device_command)
        return jsonify(status)

    def handle_control_single_device(self, control_command):

        print(control_command)
        if control_command["device_name"] == 'PHONG_KHACH' or control_command["device_name"] == 'PHONG_VE_SINH':
            self.previous_state = not self.previous_state
            print(self.previous_state)

            if self.previous_state:
                control_command['device_command'] = "ON"
            else:
                control_command['device_command'] = "OFF"
        # elif control_command["device_name"] == 'DEN_TUONG':
        #
        #     if self.previous_state:
        #         control_command['device_command'] = "ON"
        #     else:
        #         control_command['device_command'] = "OFF"

        try:
            self.esp_communication.broadcast_single_device(control_command)
        except Exception as exp:
            print(str(exp))
        status = {"message": "success"}
        return jsonify(status)

    def handle_control_multicolor_led(self, control_command):

        self.esp_communication.broadcast_single_device(control_command)
        # status = self.esp_communication.broadcast_single_device(control_command)
        status = {"message": "success"}
        return jsonify(status)

if __name__ == "__main__":
    # Function test Flask controller
    flask_controller = FlaskController()
    flask_controller.handle_all_device_status()
    flask_controller.handle_single_device_status("LED_01")
    flask_controller.handle_all_device_status()
    flask_controller.handle_all_device_status()
