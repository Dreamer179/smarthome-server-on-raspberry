__author__ = 'Edward J. C. Ashenbert'
__credits__ = ["Edward J. C. Ashenbert"]
__maintainer__ = "Edward J. C. Ashenbert"
__email__ = "nguyenquangbinh803@gmail.com"
__copyright__ = "Copyright 2020"
__status__ = "Working on demo stage 2, develop the entire local server for all raspberry"
__version__ = "1.0.1"

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from SmartHomeDevice.ESPCommunication import ESPCommunication

class ESPDataTransfer(ESPCommunication):
    def __init__(self, trasnfer_port, transfer_baudrate):
        super().__init__(trasnfer_port, transfer_baudrate)

    def fetch_energy_data_from_all(self):
        raw_data = self.read_data_from_serial()
