from microcontroller.communicator import Response
from collections import namedtuple
from globals import GlobalData
import json

def _json_object_hook(d):
    return namedtuple('X', d.keys()) (*d.values())


def json2py(param_file_json_data):
    return json.loads(param_file_json_data, object_hook=_json_object_hook)


def load_params_file(ref_LoadParamsFile, *args):
    """
        This function will return of Reference of Loaded Parameter file
        Mentioned in GlobalData
    """
    
    param_file_json_data = open(args[0]).read()
    param_file_py_data = json2py(param_file_json_data)
    
    """
        Assigning the file_is as key & file records as data in 
        Global Dictionary in GlobalData.
            
        If file is Already loaded then No need to do anything, Skip Processing
    """
    
    if param_file_py_data.file_id not in GlobalData.PARAMS_FILE_OBJ_HOLDER.keys():
        GlobalData.PARAMS_FILE_OBJ_HOLDER[param_file_py_data.file_id] = param_file_py_data
        print('Parameters loaded for file_id: {}'.format(param_file_py_data.file_id))
    else:
        print('Parameter Already Loaded for file_id: {}, Returning loaded Parameters'.format(param_file_py_data.file_id))
    
    """
        Calling the Constructor of Params Load Class for 
        Creating Object of this class by Passing file_id as Argument.
            
        If It's object have been created already then Object reference
        will be picked from Global Dictionary and file_id will be appended in it.
    """
    
    if ref_LoadParamsFile not in GlobalData.PARAMS_FILE_OBJ_HOLDER.keys():
        GlobalData.PARAMS_FILE_OBJ_HOLDER[ref_LoadParamsFile] = ref_LoadParamsFile(GlobalData.PARAMS_FILE_OBJ_HOLDER[param_file_py_data.file_id])
    else:
        GlobalData.PARAMS_FILE_OBJ_HOLDER[ref_LoadParamsFile].load_param_list.append(GlobalData.PARAMS_FILE_OBJ_HOLDER[param_file_py_data.file_id])
        print('Load Param File has an Object Already Created, Skipping Constructor call')
        
    return GlobalData.PARAMS_FILE_OBJ_HOLDER[param_file_py_data.file_id]

    
def singelton(ref_LoadParamsFile):
    def onCall(*args):
        return load_params_file(ref_LoadParamsFile, *args)
    return onCall


@singelton
class LoadParamsFile(object):
    """
        Class will load the Parameter files for Application
        Also below list will have file_id of all the loaded Parameter files
    """
    load_param_list=[]
    def __init__(self, param_file_id):
        print('Inside LoadParamsFile Constructor')
        self.load_param_list.append(param_file_id)
        print('list content is :{}'.format(self.load_param_list))


class MicroParameters(object):
    """
        This Class will loads all Parameter files for MicroController Module
    """
    def __init__(self):
        pass
    
    def get_device_params_file_name(self):
        return GlobalData.DEVICE_PARAMS_FNAME
    
    def get_device_states_file_name(self):
        return GlobalData.DEVICE_STATES_FNAME
    
    def get_device_type_id2states_file_name(self):
        return GlobalData.DEVICE_TYPE_ID2STATES_FNAME
    
    def get_microcontroller_params_file_name(self):
        return GlobalData.MICROCONTROLLER_PARAMS_FNAME
    
    def get_microcontroller_signals_file_name(self):
        return GlobalData.MICROCONTROLLER_SIGNALS_FNAME
        
    def get_device_type_id(self):
        return 0
    
    def get_micontroller_id(self):
        return 0
    
    def get_hex_device_id_signal(self):
        return 0 
    
    def get_hex_device_state_signal(self):
        return 0
    
    def get_hex_microcontroller_signal(self):
        return 0


class Microcontroller(object):
    """
        Main GPIO Class for MicroController Device
    """
    def __init__(self):
        print('Inside Microcontroller Constructor')
        
    def send_data(self):
        print('Data sent to microcontroler Programs')
        
        
class MicrocontrollerInterface(object):
    '''
        This is the Core Important class of whole Module.
        Here Only Specific task will be performed according
        to given Request Message and Response Will be Routed
        to Response Parser Module
    '''
    def __init__(self):
        print('In MicrocontrollerInterface Class in Executor')

    def process(self, mc_request):
        
        device_id=mc_request.device_id
        desired_device_state=mc_request.desired_device_state
        
        mc_param_obj = MicroParameters()
        """
            Loading Device Parameters
        """
        device_param_file=mc_param_obj.get_device_params_file_name()
        ref_device_param=LoadParamsFile(device_param_file)
        print(ref_device_param)
        """
            Loading Device Parameters
        """
        device_state_file=mc_param_obj.get_device_states_file_name()
        ref_device_state=LoadParamsFile(device_state_file)
        print(ref_device_state)
        """
            print(GlobalData.PARAMS_FILE_OBJ_HOLDER.keys())
        """
        """
            Loading Device Parameters
        """
        device_type_id2states_file=mc_param_obj.get_device_type_id2states_file_name()
        ref_device_type_id2states=LoadParamsFile(device_type_id2states_file)
        print(ref_device_type_id2states)
        """
            print(GlobalData.PARAMS_FILE_OBJ_HOLDER.keys())
        """
        """
            Loading Device Parameters
        """
        mc_param_file=mc_param_obj.get_microcontroller_params_file_name()
        ref_mc_param=LoadParamsFile(mc_param_file)
        print(ref_mc_param)
        """
            print(GlobalData.PARAMS_FILE_OBJ_HOLDER.keys())
        """
        """
            Loading Device Parameters
        """
        mc_signal_file=mc_param_obj.get_microcontroller_signals_file_name()
        ref_mc_signal=LoadParamsFile(mc_signal_file)
        print(ref_mc_signal)
        """
            print(GlobalData.PARAMS_FILE_OBJ_HOLDER.keys())
        """
        """
            For Time being HardCoded Positive Acknowledgement have been
            sent back.
            At time of actual Processing, please change Accordingly
        """
        mc_response = Response()
        mc_response.response_message = "OK"
        return mc_response