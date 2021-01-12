#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from SmartHomeServerLayer1.FlaskAppServer import *
from SmartHomeAssistant.SmartHomeManager import SmartHomeManager
import threading
# File path is not absolute that make the relative path fail

class DeployServerLayer1:
    def __init__(self):
        self.friday = SmartHomeManager()

        threading.Thread(target=self.thread_assistant).start()
        # threading.Thread(target=self.deploy_server_layer1)

    def thread_assistant(self):
        self.friday.assistant_main_assist()

    def deploy_server_layer1(self):
        app.run(host='0.0.0.0')

if __name__ == "__main__":
    deploy = DeployServerLayer1()
    deploy.deploy_server_layer1()


