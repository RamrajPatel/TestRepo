'''
    Created on 19-Aug-2014
    @author: Ashim
'''

import sys
import socket
from tcpresponsedispatcher.executor import  BasicTcpResponseDispatcher

class OutputMessage(object):
    socket_context=None
    message_bytes=None

    def __init__(self, socket_context, message_bytes):
        self.socket_context=socket_context
        self.message_bytes=message_bytes


class Request(object):
    output_message = None
    
    def __init__(self, output_message):
        self.output_message = output_message


class Response(object):
    pass


class Router(object):
    def __init__(self):
        pass
    
    def execute(self, req_tcp_res_disp_obj):
        print('executing Router Response Dispatcher')
        rd = BasicTcpResponseDispatcher()
        try:
            rd.send_reply(req_tcp_res_disp_obj)
        except (AttributeError, TypeError, socket.error) as err_message:
            print('In execute method of response Dispatcher Communicator')
            print('Data sending Failed, Reason:', err_message)
            sys.exit()