import sys
from microcontroller.executor import MicrocontrollerInterface
from microcontroller.errorhandler import MicroControllerException

def process_failure(error_source, error_type, error_msg):
    mc_exception_obj = MicroControllerException(error_source, error_type, error_msg)
    mc_exception_obj.process_exception()

class Request:
    def __init__(self, device_name, device_id, desired_device_state):
        self.device_name=device_name
        self.device_id=device_id
        self.desired_device_state=desired_device_state
        
        
class Router(object):
    def __init__(self):
        pass
    
    def execute(self, mc_request):
        """
            Here Response Object Has been Passed to executor Module so that it can have
            Return Response of that Module and can be returned back to Service Module.
            Since Communicator is importing Executor MicrocontrollerInterface Class
            and we have to use Response in same class in executor So Communicator can't
            be imported there. That's why it is being passed at time of Calling
            process() itself.
        """
        print('executing MicroController Router\'s execute function')
        try:
            mc_interface = MicrocontrollerInterface()
            resp_obj = Response()
            mc_response = mc_interface.process(mc_request, resp_obj)
        except:
            error_source="execute method in Communicator of MicroController"
            error_type=sys.exc_info()[0].__name__
            error_msg="Unexpected Error while Triggering MicroController executor"
            process_failure(error_source, error_type, error_msg)
        return mc_response


class Response(object):
    def __init__(self):
        pass