FETCH_ALL_DEVICE_STATUS = "5"
FETCH_SINGLE_DEVICE_STATUS = "4"
GET_ALL_DEVICE_DESCRIPTION = "1"
BROADCAST_ALL_DEVICE = "9"
BROADCAST_SINGLE_DEVICE = "8"

EOF = "_;"
DELIMITER = ","
SPACE = " "

LIST_OF_KEYS = ["message", "device_id", "device_name", "device_type", "device_status"]
SUCCESS_MESSSAGE = "success"
FAILURE_MESSSAGE = "failure"
LIST_OF_CODE = {"CANNOT_FOUND_DEVICE": 401, "TRANSMIT_MESSAGE_SUCCESS": 400, "BINDING_SUCCESS": 200, "TRANSMIT_MESSAGE_FAILURE": 399}
# LIST_OF_CODE = [{"CODE": 401, "MESSAGE": "CANNOT_FOUND_DEVICE"}, {"CODE": 400, "MESSAGE": "TRANSMIT_MESSAGE_SUCCESS"},
#                 {"CODE": 200, "MESSAGE": "BINDING_SUCCESS"}, {"CODE": 399, "MESSAGE": "TRANSMIT_MESSAGE_FAILURE"}]

"""
Command:
+ Turn on/off all led: "9,<ON/OFF>_;"
+ Turn on/off single led: "8,<LED_1_ON/LED_1_OFF/LED_2_ON/LED_2_OFF>_;"

============================= Request from Server to Serial =============================

+ COMMAND TYPE                      CONTENT
+ Fetch single device info:       "4,<device_name>_;"
+ Fetch all device info:          "5_;"
+ Broadcast single device:          "8,<device_name>,<device_command>_;"
+ Broadcast all device:             "9,<device_command>_;"

DESCRIPTION:
<device_name>           ==> <PHONG_NGU/PHONG_KHACH/NHA_VE_SINH/BAN_CONG>
<device_command>        ==> <ON/OFF>                    (device: ONOFF)
                            <WHITE/ORANGE/YELLOW/OFF>   (device: COLOR)
                            <#000000 ~ #FFFFFF>         (device: MULTI_COLOR)

NOTE
"_" là ký tự đặc biệt phải có để tránh command content bị sai

============================= Reponse from Serial to Server =============================

+ COMMAND TYPE                      CONTENT
+ Fetch single device info:         "<messages>,<device_id>,<device_name>,<device_type>,<device_status>;"
+ Fetch all device info:            "<messages>,<device_id>,<device_name>,<device_type>,<device_status>;<messages>,<device_name>,<device_type>,<device_status>; ..."
+ Broadcast single device:          "<messages>,<device_id>,<device_name>,<device_type>,<device_status>;"
+ Broadcast all device:             "<messages>,<device_id>,<device_name>,<device_type>,<device_status>;<messages>,<device_name>,<device_type>,<device_status>; ..."

DESCRIPTION
<device_command>        ==> <ON/OFF/WHITE/ORANGE/YELLOW/OFF>
<device_name>           ==> <PHONG_NGU/PHONG_KHACH/NHA_VE_SINH/BAN_CONG>
<device_type>           ==> <ONOFF/COLOR/MULTI_COLOR>
<messages>              ==> <success/failure>
<device_status>         ==> <ON/OFF/WHITE/ORANGE/YELLOW/OFF>

NOTE
"_" là ký tự đặc biệt phải có để tránh command content bị sai


"""
