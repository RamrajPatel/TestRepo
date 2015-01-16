'''
    Created on 14-Aug-2014
    @author: Ashim
'''

import sys
from globals import GlobalData
import services.getalldevices.communicator as gad_comm
import services.changedevicestate.communicator as cds_comm
from requestrouter.errorhandler import ReqRouterException

def process_failure(error_source, error_type, error_msg):
    req_router_exception_obj = ReqRouterException(error_source, error_type, error_msg)
    req_router_exception_obj.process_exception()


class BasicRequestRouter(object):
    '''
        BasicRequestRouter Class of Request Router Executor Module
        It will Route the incoming request to Specific
        Service Module to Perform Specific Task.
    '''
    def __init__(self):
        print('Inside Constructor of BasicRequestRouter')
        
    def route(self, req_router_request_obj):
        print('Inside Request Router route method')
        self.identify_and_call_service(req_router_request_obj)
        
    def get_service_name(self, req_router_request_obj):
        return req_router_request_obj.session.message.message_data.comm_msg.routing_info.service_info.service_name
        
    def initiate_getalldevice_service(self, req_router_request_obj):
        session = req_router_request_obj.session
        req_getalldevice_msg_obj = gad_comm.Request(session)
        router_getalldevice_obj = gad_comm.Router()
        router_getalldevice_obj.execute(req_getalldevice_msg_obj)
        
    def initiate_changedevicestate_service(self, req_router_request_obj):
        session = req_router_request_obj.session
        req_getalldevice_msg_obj = cds_comm.Request(session)
        router_getalldevice_obj = cds_comm.Router()
        router_getalldevice_obj.execute(req_getalldevice_msg_obj)
        
    def identify_and_call_service(self, req_router_request_obj):
        try:
            req_service_name = self.get_service_name(req_router_request_obj)
        except AttributeError as req_router_error_msg:
            error_source="identify_and_call_service method in Executor of RequestRouter"
            error_type=req_router_error_msg.__class__.__name__
            error_msg="AttributeError while fetching Service name from Input Request"
            process_failure(error_source, error_type, error_msg)
        except:
            error_source="identify_and_call_service method in Executor of RequestRouter"
            error_type=sys.exc_info()[0].__name__
            error_msg="Unexpected Error while fetching service name"
            process_failure(error_source, error_type, error_msg)
            
        if req_service_name == GlobalData.SERVIE_GET_ALL_DEVICES:
            print('calling get all device service')
            try:
                self.initiate_getalldevice_service(req_router_request_obj)
            except:
                error_source="identify_and_call_service method in Executor of RequestRouter"
                error_type=sys.exc_info()[0].__name__
                error_msg="Unexpected Error while initiating get all device request"
                process_failure(error_source, error_type, error_msg)
                
        elif req_service_name == GlobalData.SERVICE_CHANGE_DEVICE_STATE:
            print('calling change device state services')
            try:
                self.initiate_changedevicestate_service(req_router_request_obj)
            except:
                error_source="initiate_changedevicestate_service method in Executor of RequestRouter"
                error_type=sys.exc_info()[0].__name__
                error_msg="Unexpected Error while initiating change device state request"
                process_failure(error_source, error_type, error_msg)
        else:
            print('Invalid Service Request')
            ''' Raise Error For Invalid Service Request'''