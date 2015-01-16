'''
    Created on 14-Aug-2014
    @author: Ashim
'''

import sys
from services.changedevicestate.executor import ChangeDeviceState
from services.changedevicestate.errorhandler import SerCdsException

def process_failure(error_source, error_type, error_msg):
    ser_cds_exception_obj = SerCdsException(error_source, error_type, error_msg)
    ser_cds_exception_obj.process_exception()

class Request:
    session=None
    
    def __init__(self, session):
        self.session=session

        
class Router(object):
    def __init__(self):
        pass
    
    def execute(self, req_change_device_state_obj):
        print('executing Router Service Change Device State')
        try:
            change_device_state_obj = ChangeDeviceState()
            change_device_state_obj.process(req_change_device_state_obj)
        except:
            error_source="excute method in Communicator of Service Change Device State"
            error_type=sys.exc_info()[0].__name__
            error_msg="Unexpected Error while Triggering Service Change Device State"
            process_failure(error_source, error_type, error_msg)


class Response(object):
    pass