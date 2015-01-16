import sys
import json
import uuid                 # For Generating Random String for Incoming Request
from globals import GlobalData
from collections import namedtuple
from authenticator.communicator import Router
from authenticator.communicator import Request
from authenticator.communicator import Message
from requestparser.errorhandler import ReqParserException

'''
Created on 14-Aug-2014

@author: Ashim
'''

def process_failure(error_source, error_type, error_msg):
    req_parser_exception_obj = ReqParserException(error_source, error_type, error_msg)
    req_parser_exception_obj.process_exception()

class Decoder(object):
    '''
        This class will convert Input JSON Request into Python Object
    '''
    
    decode_input_message=None
    
    def __init__(self):
        print('Inside Decoder Class')
        
    def decode_json(self, input_message):
        try:
            decode_input_message = json.loads(input_message, object_hook=self._json_object_hook)
        except ValueError as req_parse_error_msg:
            error_source="decode_json method in Executor of RequestParser"
            error_type=req_parse_error_msg.__class__.__name__
            error_msg="ValueError in decoding JSON, Please Contact with Support Team"
            process_failure(error_source, error_type, error_msg)
        except AttributeError as req_parse_error_msg:
            error_source="decode_json method in Executor of RequestParser"
            error_type=req_parse_error_msg.__class__.__name__
            error_msg="AttributeError in decoding JSON, Please Contact with Support Team"
            process_failure(error_source, error_type, error_msg)
        except:
            error_source="decode_json method in Executor of RequestParser"
            error_type=sys.exc_info()[0].__name__
            error_msg="Unexpected Error while decoding JSON, Please Contact with Support Team"
            process_failure(error_source, error_type, error_msg)
            
        return decode_input_message

    def _json_object_hook(self, input_message):
        return namedtuple('X', input_message.keys())(*input_message.values())


class BasicRequestParser(object): 
    '''
        Request Parser Executor Class to Parse the Actual 
        Client Input Request Message
    '''
    def __init__(self):
        pass
    
    def getMessageId(self):
        """
            Write logic to generate a key for storing data and session
            and return it to program
        """
        #return 1
        message_id = str(uuid.uuid4())
        message_id = message_id.replace("-","")
        print('Generated Message Id:', message_id)
        return message_id
    
    def parse(self, input_request):
        print('Inside parsing Method')
        input_msg = input_request.input_message.message_bytes.decode('UTF-8')  
        
        '''
            Generate MessageID  and Store Socket Object To Send data
        ''' 
        try:
            message_id = self.getMessageId()
            print('Message Id for this Request is:', message_id)
            #GlobalData.store_socket[self.getMessageId()] = input_request.input_message.socket_context
            GlobalData.store_socket[message_id] = input_request.input_message.socket_context
        except AttributeError as soc_context_error_msg: 
            error_source="parse method in Executor of RequestParser"
            error_type=soc_context_error_msg.__class__.__name__
            error_msg="AttributeError while Fetching Socket Context"
            process_failure(error_source, error_type, error_msg)
        except:
            error_source="parse method in Executor of RequestParser"
            error_type=sys.exc_info()[0].__name__
            error_msg="Unexpected Error while Fetching Socket Context, Please Contact with Support Team"
            process_failure(error_source, error_type, error_msg)
            
        '''
            Prepare Authenticator Request Message and Call Authenticator
        ''' 
        decoded_input_message = Decoder().decode_json(input_msg)
        #auth_message= Message(decoded_input_message, 1)
        auth_message= Message(decoded_input_message, message_id)
        auth_request_obj = Request(auth_message)
        auth_router_obj = Router()
        auth_router_obj.execute(auth_request_obj)