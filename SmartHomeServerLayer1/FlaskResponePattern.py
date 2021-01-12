
device = [{'name': 'LED_1', 'type': 'COLOR_LED'},
          {'name': 'LED_2', 'type': 'LED'},
          {'name': 'LED_3', 'type': 'LED'},
          {'name': 'LED_4', 'type': 'COLOR_LED'}]

control_response = [{"message": "control success",
                     "name_device": "<name_device>",
                     "status_device": "<ON/OFF/WHITE/ORANGE/YELLOW/OFF>"
                     }]

control_single_device_request = {"device_id": "123", "device_name": "LED_01", "device_command": "ON"}
control_all_device_request = {"device_command": "ON"}

LIST_OF_URL = {"control_all_device": "http://127.0.0.1:5000/control_all_device", "control_single_device":
    "http://192.168.3.112:5000/control_single_device"}

# *Scan thông tin tất cả thiết bị (GET): "http://127.0.0.1:5000/get_devices_info"
Json_response = {"message": "<message>",
                 "devices": [{'device_id': "<device_id>", 'device_name': '<device_name>', 'device_type': '<device_type>',
                              'device_status': '<device_status>'},
                             {'device_id': "<device_id>", 'device_name': '<device_name>', 'device_type': '<device_type>',
                              'device_status': '<device_status>'},
                             {'device_id': "<device_id>", 'device_name': '<device_name>', 'device_type': '<device_type>',
                              'device_status': '<device_status>'},
                             {'device_id': "<device_id>", 'device_name': '<device_name>', 'device_type': '<device_type>',
                              'device_status': '<device_status>'}
                             ]
                 }

# * Điều khiển single device(PUT): "http://127.0.0.1:5000/control_single_device/"
Json_request = {"device_id": "<device_id>",
                "device_name": "<device_name>",
                "device_command": "<device_command>"
                }

Json_response = {"message": "<message>",
                 "device_id": "<device_id>",
                 "device_name": "<device_name>",
                 'device_type': '<device_type>',
                 "device_status": "<device_status>"
                 }

# * Điều khiển đèn màu RGB (PUT): "http://127.0.0.1:5000/control_multicolor_led"
Json_request = {"device_id": "<device_id>",
                "device_name": "<device_name>",
                "device_command": "<device_command>",
                "device_status": "<device_status>",
                }

Json_response = {"message": "<message>",
                 "device_id": "<device_id>",
                 "device_name": "<device_name>",
                 'device_type': '<device_type>',
                 "device_status": "<device_status>"
                 }

'''
==> chuyển sang dùng chung 1 lệnh PUT ở trên, chỗ này bình xem lại coi để sao hợp lý rồi nói ông Duy nha
==> Control all device trên app cùng lúc ko cần thiết nên Đạt bỏ phần đó, control all device giọng nói vẫn giữ (chỉ ON/OFF), đèn màu thì bỏ qua


* DESCRIPTION:
<device_id>             ==> <0 ~ 999>
<device_name>           ==> <PHONG_NGU/PHONG_KHACH/NHA_VE_SINH/BAN_CONG>
<device_type>           ==> <ONOFF/COLOR/MULTI_COLOR>
<device_command>        ==> <ON/OFF>                   (device: ONOFF)
                            <WHITE/ORANGE/YELLOW/OFF>  (device: COLOR)
                            <CONTROL_COLOR>        (device: MULTI_COLOR)
<message>              ==> <success/failure>
<device_status>         ==> <ON/OFF>                    (device: ONOFF)
                            <WHITE/ORANGE/YELLOW/OFF>   (device: COLOR)
                            <#000000 ~ #FFFFFF>         (device: MULTI_COLOR)
'''
