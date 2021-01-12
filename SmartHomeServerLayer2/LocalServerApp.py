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

from SmartHomeServerLayer2.LocalServerController import LocalServerController

app = Flask(__name__)
flask_controller = LocalServerController()

@app.route('/', methods=['GET'])
def server_start():
    return jsonify({'message': 'This is Hotel Server'})

@app.route('/send_ultimate_command', methods=["PUT"])
def send_ultimate_command(command_type="http"):
    if command_type == "http":
        control_command = request.get_json()
        if control_command:
            print("Get JSON: ", control_command)
            return flask_controller.send_ultimate_command(control_command)
        else:
            print("message: No JSON was sent to server")
            return jsonify({'message': "No JSON was sent to server"})
    elif command_type == "gui":
        control_command = request.get_json()
        if control_command:
            print("Get JSON: ", control_command)
            return flask_controller.send_ultimate_command(control_command)
        else:
            print("message: No JSON was sent to server")
            return jsonify({'message': "No JSON was sent to server"})




if __name__ == "__main__":
    app.run(host='0.0.0.0')
