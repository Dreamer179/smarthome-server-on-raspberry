__author__ = 'Edward J. C. Ashenbert'
__credits__ = ["Edward J. C. Ashenbert"]
__maintainer__ = "Edward J. C. Ashenbert"
__email__ = "nguyenquangbinh803@gmail.com"
__copyright__ = "Copyright 2020"
__status__ = "Working on demo stage 1"
__version__ = "1.0.1"

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from flask import jsonify
from flask import request

from SmartHomeServerLayer1.FlaskAppController import FlaskAppController

app = Flask(__name__)
flask_controller = FlaskAppController()

@app.route('/', methods=['GET'])
def server_start():
    return jsonify({'message': 'This is Smart Home Server'})

@app.route('/get_single_device_data/<string:name>', methods=['GET'])
def get_device_data(name):
    return flask_controller.handle_single_device_status(name)

@app.route('/get_devices_info', methods=['GET'])
def get_all_device_data():
    print("get_devices_info")
    return jsonify(flask_controller.handle_all_device_info())

@app.route('/control_all_device', methods=['GET', "PUT"])
def control_all_device():
    control_command = request.get_json()
    if control_command:
        print("Get JSON: ", control_command)
        return jsonify(flask_controller.handle_control_all_device(control_command))
    else:
        return jsonify({'message': "No JSON was sent to server"})

@app.route('/control_curtain', methods=["POST"])
def control_curtain():
    control_command = request.get_json()
    if control_command:
        print("Get JSON: ", control_command)
        return jsonify(flask_controller.handle_control_curtain(control_command))
    else:
        return jsonify({'message': "No JSON was sent to server"})

@app.route('/control_single_device', methods=[ "PUT"])
def control_single_device():
    control_command = request.get_json()
    print(control_command)
    if control_command:
        print("Get JSON: ", control_command)
        return jsonify(flask_controller.handle_control_single_device(control_command))
    else:
        return jsonify({'message': "No JSON was sent to server"})

@app.route('/control_multicolor_led', methods=["PUT"])
def control_multicolor_led():
    control_command = request.get_json()
    if control_command:
        print("Get JSON: ", control_command)
        return jsonify(flask_controller.handle_control_multicolor_led(control_command))
    else:
        print("message: No JSON was sent to server")
        return jsonify({'message': "No JSON was sent to server"})

if __name__ == "__main__":
    app.run(host='0.0.0.0')
