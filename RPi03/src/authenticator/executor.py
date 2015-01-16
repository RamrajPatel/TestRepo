from requestrouter.communicator import Router
from requestrouter.communicator import Session
from requestrouter.communicator import Request
from authenticator.errorhandler import AuthenticatorException

'''
Created on 14-Aug-2014

@author: Ashim
'''

def process_failure(error_source, error_type, error_msg):
    authenticator_exception_obj = AuthenticatorException(error_source, error_type, error_msg)
    authenticator_exception_obj.process_exception()
    '''
        Exception Not yet Implemented here, Left for Future :P :D :)
    '''

class BasicAuthenticator:
    '''
        This Class will authenticates Input Request and Prepare
        Request Router Triggering MetaData
    '''
    def __init__(self):
        print('In Basic Authenticator')
        
    def authenticate(self, auth_req_obj):
        print('Inside Authenticate function of BasicAuthenticator')
        self.validate_credentials()
        self.prepare_msg(auth_req_obj.message)
        
    def validate_credentials(self):
        print('Inside Validate Credentials function')
        
    def prepare_msg(self,Input_Msg):
        print('Inside prepare Message, Calling Request Router Module')
        SessionId = 'Sess1'
        '''Message = Input_Msg'''
        Permission = 'TRUE'
        print('Preparing Session for Request Router Object')
        session = Session(SessionId, Input_Msg, Permission)
        print('Preparing Request Object for Request Router Request Class')
        req_router_request_obj = Request(session)
        req_router_router_obj = Router()
        print('Calling execute function of Request Router ')
        req_router_router_obj.execute(req_router_request_obj)
        print('Router execute method called by Authenticator')