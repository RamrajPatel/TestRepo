'''
    Created on 14-Aug-2014
    @author: Ashim
'''

import sys
from services.getalldevices.executor import GetAllDevices
from services.getalldevices.errorhandler import SerGadException

def process_failure(error_source, error_type, error_msg):
    ser_gad_exception_obj = SerGadException(error_source, error_type, error_msg)
    ser_gad_exception_obj.process_exception()

class Request:
    session=None
    
    def __init__(self, session):
        self.session=session
        

class Router(object):
    def __init__(self):
        pass
    
    def execute(self, req_getalldevice_msg_obj):
        print('executing Router Get All Devices List')
        try:
            getalldevices_obj = GetAllDevices()
            getalldevices_obj.process(req_getalldevice_msg_obj)
        except:
            error_source="excute method in Communicator of Service GAD"
            error_type=sys.exc_info()[0].__name__
            error_msg="Unexpected Error while Triggering Service GAD"
            process_failure(error_source, error_type, error_msg)


class Response(object):
    pass