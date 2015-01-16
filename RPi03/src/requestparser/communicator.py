'''
    Created on 18-Aug-2014

    @author: Ashim
'''

import sys
import time
import queue
from requestparser.executor import BasicRequestParser
from requestparser.errorhandler import ReqParserException
from globals import GlobalData

queueObj=queue.Queue(50)

def process_failure(error_source, error_type, error_msg):
    req_parser_exception_obj = ReqParserException(error_source, error_type, error_msg)
    req_parser_exception_obj.process_exception()

class InputMessage(object):
    '''
        This Class will store Input Client Request Message
        and Other Meta Data like Dispatcher ID and socket Context
    '''
    dispatcher_id=None
    message_bytes=None
    socket_context=None
    
    def __init__(self, dispatcher_id, message_bytes, socket_context):
        self.dispatcher_id=dispatcher_id
        self.message_bytes=message_bytes
        self.socket_context=socket_context	


class InputStore(object):
    def __init__(self):
        print('Inside init of InputStore class')
    
    def schedule_request(self, request, queueObj):
        queueObj.put(request)
        print('Input Request: ', request)
        time.sleep(1)


class FetchRequest(object):
    def __init__(self):
        print('Inside init of FetchRequest class')
        
    def get_request(self):
        time.sleep(1)
        while not queueObj.empty():
        #while True:
            data = queueObj.get()
            print('Fetch Request: ', data)
            time.sleep(2)
            #queueObj.task_done()
        print('Exiting from FetchRequest')
        '''
            To avoid sleep() function, we need to put a infinite loop
            over request Queue to scan input request continuously.
            We can also make a Listener class for the same purpose
        '''


class Request(object):
    '''
        Request class of RequestParser Module. It's Object
        will be sent as Argument to execute function in Router
        to Process Next
    '''
    input_message=None
    
    def __init__(self, input_message):
        self.input_message=input_message


class Response(object):
    pass


class Router(object):
    '''
        Router Class of RequestParser Module. This will be
        route the Request Object of Request Parser for 
        further Processing
    '''
    def __init__(self):
        pass
    
    def execute(self, input_request):
        
        try:
            req_parse_exe_obj = BasicRequestParser()
            req_parse_exe_obj.parse(input_request)
        except:
            error_source="execute method in Communicator of RequestParser"
            error_type=sys.exc_info()[0].__name__
            error_msg="Unexpected Error while Triggering Request Parser executor"
            process_failure(error_source, error_type, error_msg)


class SocketContext(object):
    '''
        SocketContext class of Request Parser Module 
        Used to Store Connection Details Only
    '''
    def __init__(self, connection_details):
        self.connection_details = connection_details