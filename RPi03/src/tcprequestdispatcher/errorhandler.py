from responseparser.communicator import Request
from responseparser.communicator import Router

class ReqDispatcherException(object):
    error_source=""
    error_type=""
    error_msg=""
    #error_code=0
    
    def __init__(self, error_source, error_type, error_msg):
        #self.error_code=error_code
        self.error_msg=error_msg
        self.error_source=error_source
        self.error_type=error_type
        
    def process_exception(self):
        print('Inside process_exception method of ReqDispatcherException')
        self.trigger_response()
    
    def trigger_response(self):
        print('Inside trigger_response method of ReqDispatcherException')
        req_res_parser_obj = Request(self, "ERROR")
        router_res_parser_obj = Router()
        router_res_parser_obj.execute(req_res_parser_obj)