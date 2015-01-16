'''
    Created on 19-Aug-2014
    @author: Ashim
'''

import sys
from authenticator.executor import BasicAuthenticator
from authenticator.errorhandler import AuthenticatorException

def process_failure(error_source, error_type, error_msg):
    authenticator_exception_obj = AuthenticatorException(error_source, error_type, error_msg)
    authenticator_exception_obj.process_exception()

class Message(object):
    '''
        class will hold Input Message and Message ID associated 
        with it.
    '''
    message_data=None
    message_id=None

    def __init__(self, message_data, message_id):
        self.message_data=message_data
        self.message_id=message_id
        
        
class Request(object):
    '''
       this is the message object which RequestPraser has
       to sent in its response, if this changes then 
       RequestParser reponse will have to be changed as well
    '''
    
    message=None
    
    def __init__(self, message):
        self.message=message
        

class Response(object):
    pass


class Router(object):
    '''
        Router will route the Input Message Request to 
        Authenticator(Executor Module of Authenticator)
        Module to Authenticate the Request 
        Before Actual Processing of Message 
    '''

    def __init__(self):
        pass
        
    def execute(self, auth_req_obj):
        try:
            auth_exec_obj = BasicAuthenticator()
            auth_exec_obj.authenticate(auth_req_obj)
        except:
            error_source="excute method in Communicator of Authenticator"
            error_type=sys.exc_info()[0].__name__
            error_msg="Unexpected Error while Triggering Authenticator executor"
            process_failure(error_source, error_type, error_msg)