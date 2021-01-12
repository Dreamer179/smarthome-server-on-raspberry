__author__ = 'Edward J. C. Ashenbert'
__credits__ = ["Edward J. C. Ashenbert"]
__maintainer__ = "Edward J. C. Ashenbert"
__email__ = "nguyenquangbinh803@gmail.com"
__copyright__ = "Copyright 2020"
__status__ = "Working on demo stage 2, develop the entire local server for all raspberry"
__version__ = "1.0.1"

import requests
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

if __name__ == "__main__":
    available_room = []
    for i in range(1,2):
        for j in range(256):
            try:
                ip_address = "http://192.168." + str(i) + "." + str(j) + ":5000/"
                res = requests.get("http://192.168." + str(i) + "." + str(j) + ":5000/", timeout=0.001)
                if res.ok:
                    available_room.append(ip_address)

            except Exception as exp:
                print(str(exp))
                pass
    print(available_room)
