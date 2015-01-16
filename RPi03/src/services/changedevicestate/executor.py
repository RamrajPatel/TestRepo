'''
    Created on 14-Aug-2014
    @author: Ashim
'''

import sys
import responseparser.communicator as resp_comm
import microcontroller.communicator as mc_comm
from services.changedevicestate.errorhandler import SerCdsException

def process_failure(error_source, error_type, error_msg):
    ser_cds_exception_obj = SerCdsException(error_source, error_type, error_msg)
    ser_cds_exception_obj.process_exception()

class SerOneOutMsg(object):
    outputDictString={"comm_msg": {}}
    def __init__(self):
        print('init here in SerOneMsg')
        
        
class ChangeDeviceState(object):
    '''
        This is the Core Important class of whole Module.
        Here Only Specific task will be performed according
        to given Request Message and Response Will be Routed
        to Response Parser Module
    '''
    def __init__(self):
        print('In Change Device State Constructor')
    
    def get_device_name(self, input_request):
        return input_request.comm_msg.routing_info.service_info.service_request.device_name
    
    def get_device_id(self, input_request):
        return input_request.comm_msg.routing_info.service_info.service_request.device_id
    
    def get_desired_device_state(self, input_request):
        return input_request.comm_msg.routing_info.service_info.service_request.desired_device_state
    
    def process(self, req_change_device_state_obj):
        print('Inside Change Device State Process')
        try:
            input_request = req_change_device_state_obj.session.message.message_data
            input_request_id = req_change_device_state_obj.session.message.message_id
        except AttributeError as ser_cds_error_msg: 
            error_source="process method in Executor of CDS Service"
            error_type=ser_cds_error_msg.__class__.__name__
            error_msg="AttributeError while Fetching Input Data or MetaData"
            process_failure(error_source, error_type, error_msg)
        except:
            error_source="process method in Executor of CDS Service"
            error_type=sys.exc_info()[0].__name__
            error_msg="Unexpected Error while Fetching Input Data or MetaData"
            process_failure(error_source, error_type, error_msg)    
        print('message from Client in CDS Service:' , input_request)
        
        """
            Fetch Device Id & Desired State change request from Input Request 
            and Trigger MicroController Module for further Processing
        """
        try:
            device_name = self.get_device_name(input_request)
            device_id = self.get_device_id(input_request)
            desired_device_state = self.get_desired_device_state(input_request)
        except AttributeError as ser_CDS_error_msg: 
            error_source="process method in Executor of CDS Service"
            error_type=ser_CDS_error_msg.__class__.__name__
            error_msg="AttributeError while Fetching Device Info"
            process_failure(error_source, error_type, error_msg)
        except:
            error_source="process method in Executor of CDS Service"
            error_type=sys.exc_info()[0].__name__
            error_msg="Unexpected Error while Fetching Device Info"
            process_failure(error_source, error_type, error_msg)
        print('device_name is : {}'.format(device_name))
        print('device_id is : {}'.format(device_id))
        print('desired_device_state is : {}'.format(desired_device_state))
        
        '''
            Calling MicroController Module for Actual Processing
        '''
        try:
            mc_request = mc_comm.Request(device_name, device_id, desired_device_state)
            mc_router = mc_comm.Router()
            mc_response = mc_router.execute(mc_request)
        except:
            error_source="process method in Executor of CDS Service"
            error_type=sys.exc_info()[0].__name__
            error_msg="Error while MicroController Processing"
            process_failure(error_source, error_type, error_msg)
        print(mc_response)
        
        """
            This mc_response is the returned response object of MicroController
            Module. it will have Resonse message Positive or Negative.
            Further Processing will be depends on Response Message
 
            Preparing Positive Response from Change Device State Module Assuming 
            MicroController Processing is successful
        """
        try:
            output_response= SerOneOutMsg()
            output_response.outputDictString["comm_msg"]["response_stat"] = "OK"  
            print(output_response.outputDictString)

            new_session = req_change_device_state_obj
            new_session.session.message.message_data = output_response.outputDictString
            new_session.session.message.message_id = input_request_id
        except AttributeError as ser_CDS_error_msg: 
            error_source="process method in Executor of CDS Service"
            error_type=ser_CDS_error_msg.__class__.__name__
            error_msg="AttributeError while Generating Service Response"
            process_failure(error_source, error_type, error_msg)
        except:
            error_source="process method in Executor of CDS Service"
            error_type=sys.exc_info()[0].__name__
            error_msg="Unexpected Error while Generating Service Response"
            process_failure(error_source, error_type, error_msg)
        print(new_session.session.message.message_data)
        
        '''
            Calling Response Parser with Service Positive Response
        '''
        try:
            req_res_parser_obj = resp_comm.Request(new_session, "OK")
            router_res_parser_obj = resp_comm.Router()
            router_res_parser_obj.execute(req_res_parser_obj)
        except:
            error_source="process method in Executor of CDS Service"
            error_type=sys.exc_info()[0].__name__
            error_msg="Error while Calling Response Parser"
            process_failure(error_source, error_type, error_msg)