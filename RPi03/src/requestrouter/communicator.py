'''
    Created on 14-Aug-2014
    @author: Ashim
'''

import sys
from requestrouter.executor import BasicRequestRouter
from requestrouter.errorhandler import ReqRouterException

def process_failure(error_source, error_type, error_msg):
    req_router_exception_obj = ReqRouterException(error_source, error_type, error_msg)
    req_router_exception_obj.process_exception()

class Request(object):
    '''
        Request Class of Request Router.
        Accepting incoming Session Object from Authenticator
    '''

    session=None

    def __init__(self, session):
        self.session = session


class Response(object):
    pass	


class Router(object):
    '''
        Router Class of Request Router Module
    '''

    def __init__(self):
        pass
    
    def execute(self,req_router_request_obj):
        print('Inside execute method of Router Class in Request Router')
        try:
            router_exec_obj = BasicRequestRouter()
            router_exec_obj.route(req_router_request_obj)
        except:
            error_source="excute method in Communicator of RequestRouter"
            error_type=sys.exc_info()[0].__name__
            error_msg="Unexpected Error while Triggering Request Router executor"
            process_failure(error_source, error_type, error_msg)


class Session(object):
    '''
        Session Class of Request Router Module will Hold Complete 
        Session Object including Input Message
    '''
    session_id=None
    message=None  
    ''' this Message is same as Authenticators Communicators Message '''
    permission=None    

    def __init__(self, session_id, message, permission):
        self.session_id=session_id
        self.message=message
        self.permission=permission