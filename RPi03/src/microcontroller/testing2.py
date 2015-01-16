from collections import namedtuple
from globals import GlobalData
import json

def _json_object_hook(d):
    return namedtuple('X', d.keys()) (*d.values())

def json2py(param_file_json_data):
    return json.loads(param_file_json_data)

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
    
    if param_file_py_data["file_id"] not in GlobalData.PARAMS_FILE_OBJ_HOLDER.keys():
        GlobalData.PARAMS_FILE_OBJ_HOLDER[param_file_py_data["file_id"]] = param_file_py_data
        print('Parameters loaded for file_id: {}'.format(param_file_py_data["file_id"]))
    else:
        print('Parameter Already Loaded for file_id: {}, Returning loaded Parameters'.format(param_file_py_data["file_id"]))
    
    """
        Calling the Constructor of Params Load Class for 
        Creating Object of this class by Passing file_id as Argument.
            
        If It's object have been created already then Object reference
        will be picked from Global Dictionary and file_id will be appended in it.
    """
    
    if ref_LoadParamsFile not in GlobalData.PARAMS_FILE_OBJ_HOLDER.keys():
        GlobalData.PARAMS_FILE_OBJ_HOLDER[ref_LoadParamsFile] = ref_LoadParamsFile(GlobalData.PARAMS_FILE_OBJ_HOLDER[param_file_py_data["file_id"]])
    else:
        GlobalData.PARAMS_FILE_OBJ_HOLDER[ref_LoadParamsFile].load_param_list.append(GlobalData.PARAMS_FILE_OBJ_HOLDER[param_file_py_data["file_id"]])
        print('Load Param File has an Object Already Created, Skipping Constructor call')
        
    return GlobalData.PARAMS_FILE_OBJ_HOLDER[param_file_py_data["file_id"]]
    
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
        return ref_device_param["file_data"][device_id]["device_type_id"]
    
    def get_micontroller_id(self, device_id, ref_device_param):
        return ref_device_param["file_data"][device_id]["module_id"]
    
    def get_device_type_state_id(self, device_type_id, ref_device_type_id2states):
        return ref_device_type_id2states["file_data"][device_type_id]["states_id"]
    
    def get_device_signal_id(self, device_id, ref_device_param):
        return ref_device_param["file_data"][device_id]["signal_id"]
    
    def get_devcie_state_signal_id(self, device_type_state_id, desired_device_state, ref_device_state):
        """
            Implemented Fall-Back Concept
        """
        if device_type_state_id in ref_device_state["file_data"]:
            if desired_device_state in ref_device_state["file_data"][device_type_state_id]:
                return ref_device_state["file_data"][device_type_state_id][desired_device_state]["signal_id"]
            else:
                print('Mapping signal not found fetching if Default tag is Present')
                if 'default_tag' in ref_device_state["file_data"][device_type_state_id]:
                    default_tag_val = ref_device_state["file_data"][device_type_state_id]['default_tag']
                    return ref_device_state["file_data"][default_tag_val][desired_device_state]["signal_id"]
                else:
                    print('No default mapping found for this tag error')
        else:
            print('No state ID Mapping found in PArameter file')
                
    
    def get_microcontroller_signal_id(self, module_id, ref_mc_param):
        return ref_mc_param["file_data"][module_id]["signal_id"]
    
    """
    def get_hex_device_id_signal(self, device_signal_id, ref_mc_signal):
        return ref_mc_signal["file_data"][device_signal_id]["signal"]
    """
    
    def get_hex_device_id_signal(self, device_signal_id, ref_mc_signal):
        """
            Implemented Fall Back Concept
        """
        if device_signal_id in ref_mc_signal["file_data"]:
            if 'signal' in ref_mc_signal["file_data"][device_signal_id]:
                return ref_mc_signal["file_data"][device_signal_id]["signal"]
            else:
                print('Signal Mapping Not Found, Fetching from Default if any')
                if 'default_tag' in ref_mc_signal["file_data"][device_signal_id]:
                    default_tag_val = ref_mc_signal["file_data"][device_signal_id]['default_tag']
                    if device_signal_id in ref_mc_signal["file_data"][default_tag_val]:
                        return ref_mc_signal["file_data"][default_tag_val][device_signal_id]
                    else:
                        print('No Signal in File Default Tag, Error')
                else:
                    print('No Default Mapping too found for this signal, Skipping Processing, Error')
        else:
            print("No Signal found for this Signal Id, Throwing Error")
    
    """
    def get_hex_device_state_signal(self, device_state_signal_id, ref_mc_signal):
        return ref_mc_signal["file_data"][device_state_signal_id]["signal"]
    """
    
    def get_hex_device_state_signal(self, device_state_signal_id, ref_mc_signal):
        """
            Implemented Fall Back Concept For Device State MicroController Signal
        """
        print('Inside Device State Signal Method')
        if device_state_signal_id in ref_mc_signal["file_data"]:
            if 'signal' in ref_mc_signal["file_data"][device_state_signal_id]:
                return ref_mc_signal["file_data"][device_state_signal_id]["signal"]
            else:
                print('Signal Mapping Not Found, Fetching from Default if any')
                if 'default_tag' in ref_mc_signal["file_data"][device_state_signal_id]:
                    default_tag_val = ref_mc_signal["file_data"][device_state_signal_id]['default_tag']
                    if device_state_signal_id in ref_mc_signal["file_data"][default_tag_val]:
                        return ref_mc_signal["file_data"][default_tag_val][device_state_signal_id]
                    else:
                        print('No Signal in File Default Tag, Error')
                else:
                    print('No Default Mapping too found for this signal, Skipping Processing, Error')
        else:
            print("No Signal found for this Signal Id, Throwing Error")
    
    """
    def get_hex_microcontroller_signal(self, module_signal_id, ref_mc_signal):
        return ref_mc_signal["file_data"][module_signal_id]["signal"]
    """
    
    def get_hex_microcontroller_signal(self, module_signal_id, ref_mc_signal):
        """
            Implemented Fall-Back Concept for MicroController Signal
        """
        print('Inside MicroController Signal Method')
        if module_signal_id in ref_mc_signal["file_data"]:
            if 'signal' in ref_mc_signal["file_data"][module_signal_id]:
                return ref_mc_signal["file_data"][module_signal_id]["signal"]
            else:
                print('Signal Mapping Not Found, Fetching from Default if any')
                if 'default_tag' in ref_mc_signal["file_data"][module_signal_id]:
                    default_tag_val = ref_mc_signal["file_data"][module_signal_id]['default_tag']
                    if module_signal_id in ref_mc_signal["file_data"][default_tag_val]:
                        return ref_mc_signal["file_data"][default_tag_val][module_signal_id]
                    else:
                        print('No Signal in File Default Tag, Error')
                else:
                    print('No Default Mapping too found for this signal, Skipping Processing, Error')
        else:
            print("No Signal found for this Signal Id, Throwing Error")
    

class Microcontroller(object):
    """
        Main GPIO Class for MicroController Device
    """
    device_signal=None
    device_state_signal=None
    module_signal=None
    
    def __init__(self, device_signal, device_state_signal, module_signal):
        print('Inside MicroController Constructor')
        self.device_signal = device_signal
        self.device_state_signal = device_state_signal
        self.module_signal = module_signal
        
    def send_data(self):
        print('Data sent to microController Programs')
                                
if __name__=='__main__':
    device_id="DEVIBDREFAN000001"
    desired_device_state="OFF"
    mc_param_obj = MicroParameters()
    
    device_param_file=mc_param_obj.get_device_params_file_name()
    ref_device_param=LoadParamsFile(device_param_file)
    
    """
        Loading Device Type States Parameters
    """
    device_state_file=mc_param_obj.get_device_states_file_name()
    ref_device_state=LoadParamsFile(device_state_file)
    print(ref_device_state)
    """
        print(GlobalData.PARAMS_FILE_OBJ_HOLDER.keys())
    """
    """
        Loading Device Type Parameters
    """
    device_type_id2states_file=mc_param_obj.get_device_type_id2states_file_name()
    ref_device_type_id2states=LoadParamsFile(device_type_id2states_file)
    print(ref_device_type_id2states)
    """
        print(GlobalData.PARAMS_FILE_OBJ_HOLDER.keys())
    """
    """
       Loading MicroController Parameters
    """
    mc_param_file=mc_param_obj.get_microcontroller_params_file_name()
    ref_mc_param=LoadParamsFile(mc_param_file)
    print(ref_mc_param)
    """
            print(GlobalData.PARAMS_FILE_OBJ_HOLDER.keys())
    """
    """
            Loading MicroController Hardware Signals Parameters
    """
    mc_signal_file=mc_param_obj.get_microcontroller_signals_file_name()
    ref_mc_signal=LoadParamsFile(mc_signal_file)
    print(ref_mc_signal)

    
    device_type_id = mc_param_obj.get_device_type_id(device_id, ref_device_param)
        
    module_id = mc_param_obj.get_micontroller_id(device_id, ref_device_param)
        
    print('data is: {} : {} '.format(device_type_id, module_id))
    """
       Now Fetching Device Type States IDs and Signal IDs for Device,
        Device States and MicrController
    """
    device_signal_id = mc_param_obj.get_device_signal_id(device_id, ref_device_param)
        
    device_type_state_id = mc_param_obj.get_device_type_state_id(device_type_id, ref_device_type_id2states)
        
    device_state_signal_id = mc_param_obj.get_devcie_state_signal_id(device_type_state_id, desired_device_state, ref_device_state)
        
    module_signal_id = mc_param_obj.get_microcontroller_signal_id(module_id, ref_mc_param)
    """
       Finally Fetching Hardware Triggering MicrController Signal for device,
       Device state and MicroController
    """
        
    device_signal = mc_param_obj.get_hex_device_id_signal(device_signal_id, ref_mc_signal)
       
    device_state_signal = mc_param_obj.get_hex_device_state_signal(device_state_signal_id, ref_mc_signal)
        
    module_signal = mc_param_obj.get_hex_microcontroller_signal(module_signal_id, ref_mc_signal)
    print('hello done')
