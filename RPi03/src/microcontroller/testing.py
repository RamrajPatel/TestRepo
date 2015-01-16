from collections import namedtuple
from globals import GlobalData
import json

def _json_object_hook(d):
    return namedtuple('X', d.keys()) (*d.values())

def json2py(param_file_json_data):
    return json.loads(param_file_json_data, object_hook=_json_object_hook)
    #return json.loads(param_file_json_data)

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
    
    def get_device_type_id(self, device_id, ref_device_param):
        print('coming here')
        return ref_device_param.file_data.get(device_id)
        #return ref_device_param.file_data[device_id].device_id_type
    
    def get_micontroller_id(self, device_id, ref_device_param):
        return ref_device_param.file_data.device_id.module_id
        #return ref_device_param.file_data[device_id].module_id
    
    def get_device_signal_id(self, device_id, ref_device_param):
        return ref_device_param.file_data.device_id.signal_id
        #return ref_device_param.file_data[device_id].signal_id
        
                
if __name__=='__main__':
    device_id="DEVIBDREFAN000001"
    desired_device_state='OFF'
    mc_param_obj = MicroParameters()
    
    device_param_file=mc_param_obj.get_device_params_file_name()
    ref_device_param=LoadParamsFile(device_param_file)
    
    device_type_id = mc_param_obj.get_device_type_id(device_id, ref_device_param)
    print('deice is type is {}'.format(device_type_id))
    module_id = mc_param_obj.get_micontroller_id(device_id, ref_device_param)
    signal_id = mc_param_obj.get_device_signal_id(device_id, ref_device_param)
    print('data is: {} : {} : {}'.format(device_type_id, module_id, signal_id))