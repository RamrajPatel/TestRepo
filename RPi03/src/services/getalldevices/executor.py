'''
    Created on 14-Aug-2014
    @author: Ashim
'''

'''
Abbreviations:
    GAD : Get All Devices
'''

import sys
import json
from globals import GlobalData
from responseparser.communicator import Request
from responseparser.communicator import Router
from services.getalldevices.errorhandler import SerGadException

def process_failure(error_source, error_type, error_msg):
    ser_gad_exception_obj = SerGadException(error_source, error_type, error_msg)
    ser_gad_exception_obj.process_exception()

class SerOneOutMsg(object):
    outputDictString={"comm_msg": {}}
    def __init__(self):
        print('init here in SerOneMsg')
        
        
class GetAllDevices(object):
    '''
        This is the Core Important class of whole Module.
        Here Only Specific task will be performed according
        to given Request Message and Response Will be Routed
        to Response Parser Module
    '''
    def __init__(self):
        pass
    
    def get_all_devices(self):
        json_data=open(GlobalData.GET_ALL_DEVICE_LIST_FNAME).read()
        return json.loads(json_data)
    
    def process(self, req_getalldevice_msg_obj):
        print('in GetAllDevices Process')
        try:
            input_request = req_getalldevice_msg_obj.session.message.message_data
            input_request_id = req_getalldevice_msg_obj.session.message.message_id
        except AttributeError as ser_gad_error_msg: 
            error_source="process method in Executor of GAD Service"
            error_type=ser_gad_error_msg.__class__.__name__
            error_msg="AttributeError while Fetching Input Data or MetaData"
            process_failure(error_source, error_type, error_msg)
        except:
            error_source="process method in Executor of GAD Service"
            error_type=sys.exc_info()[0].__name__
            error_msg="Unexpected Error while Fetching Input Data or MetaData"
            process_failure(error_source, error_type, error_msg)
        print('message from Client in Service:' , input_request)
        
        '''
            Fetching All Devices from All Device Details Params file
        '''
        output_response= SerOneOutMsg()
        try:
            devices_details = self.get_all_devices()
        except ValueError as ser_gad_error_msg: 
            error_source="process method in Executor of GAD Service"
            error_type=ser_gad_error_msg.__class__.__name__
            error_msg="ValueError, params file load error"
            process_failure(error_source, error_type, error_msg)
        except TypeError as ser_gad_error_msg: 
            error_source="process method in Executor of GAD Service"
            error_type=ser_gad_error_msg.__class__.__name__
            error_msg="TypeError, param file load error"
            process_failure(error_source, error_type, error_msg)
        except EOFError as ser_gad_error_msg: 
            error_source="process method in Executor of GAD Service"
            error_type=ser_gad_error_msg.__class__.__name__
            error_msg="EOFError, params file is empty"
            process_failure(error_source, error_type, error_msg)
        except IOError as ser_gad_error_msg: 
            error_source="process method in Executor of GAD Service"
            error_type=ser_gad_error_msg.__class__.__name__
            error_msg="IOError, loding param file error"
            process_failure(error_source, error_type, error_msg)
        except AttributeError as ser_gad_error_msg: 
            error_source="process method in Executor of GAD Service"
            error_type=ser_gad_error_msg.__class__.__name__
            error_msg="AttributeError while Fetching Input Data or MetaData"
            process_failure(error_source, error_type, error_msg)
        except:
            error_source="process method in Executor of GAD Service"
            error_type=sys.exc_info()[0].__name__
            error_msg="Unexpected Error while Fetching Input Data or MetaData"
            process_failure(error_source, error_type, error_msg)
        print(devices_details["home_info"])
        
        '''
            Generating Response for Service Get All Devices
        '''
        try:
            output_response.outputDictString["comm_msg"]["response_stat"] = "OK"
            output_response.outputDictString["comm_msg"]["home_info"] = devices_details["home_info"]
            print(output_response.outputDictString)
            new_session = req_getalldevice_msg_obj
        
            new_session.session.message.message_data = output_response.outputDictString
            new_session.session.message.message_id = input_request_id
        except AttributeError as ser_gad_error_msg: 
            error_source="process method in Executor of GAD Service"
            error_type=ser_gad_error_msg.__class__.__name__
            error_msg="AttributeError while Generating Service Response"
            process_failure(error_source, error_type, error_msg)
        except:
            error_source="process method in Executor of GAD Service"
            error_type=sys.exc_info()[0].__name__
            error_msg="Unexpected Error while Generating Service Response"
            process_failure(error_source, error_type, error_msg)
        print(new_session.session.message.message_data)
        
        '''
            Calling Response Parser with Positive Service rsesponse
        '''
        try:
            req_res_parser_obj = Request(new_session, "OK")
            router_res_parser_obj = Router()
            router_res_parser_obj.execute(req_res_parser_obj)
        except:
            error_source="process method in Executor of GAD Service"
            error_type=sys.exc_info()[0].__name__
            error_msg="Error while Calling Response Parser"
            process_failure(error_source, error_type, error_msg)