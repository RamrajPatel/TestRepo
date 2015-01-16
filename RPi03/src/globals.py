class GlobalData(object):
    '''
        Class will hold global variable for Application
    '''
    store_socket = {}
    PARAMS_FILE_OBJ_HOLDER={}
    PARAMS_QUEUE_NAME_HOLDER={}
    HOST_IP='127.0.0.1'
    REQUEST_PORT = 8802
    DEVICE_PARAMS_FNAME='H:\RPi_Params\DeviceParams.json'
    DEVICE_STATES_FNAME='H:\RPi_Params\DevicePossibleStates.json'
    DEVICE_TYPE_ID2STATES_FNAME='H:\RPi_Params\DeviceTypeId2DevState.json'
    MICROCONTROLLER_PARAMS_FNAME='H:\RPi_Params\MicrocontrollerParams.json'
    MICROCONTROLLER_SIGNALS_FNAME='H:\RPi_Params\MicrocontrollerSignals.json'
    GET_ALL_DEVICE_LIST_FNAME='H:\RPi_Params\GetAllDevicesList.json'
    ERROR_PARAMS_FNAME='H:\RPi_Params\ErrorParams.json'
    SERVIE_GET_ALL_DEVICES='GetAllDevice'
    SERVICE_CHANGE_DEVICE_STATE='ChangeDeviceState'

    
    def __init__(self):
        pass