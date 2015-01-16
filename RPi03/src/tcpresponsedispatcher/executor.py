import sys
import socket

class BasicTcpResponseDispatcher(object):
    """
        This is Final Class that will send data Response to Client
        Data will be sent in form of byte string
    """
    def __init__(self):
        pass
        
    def send_reply(self, req_tcp_res_disp_obj):
        print('in Send_Reply in BasicTcpResponseDispatcher ')
        try:
            socket_context = req_tcp_res_disp_obj.output_message.socket_context
        except (AttributeError, TypeError) as err_message:
            print('Res Dispatcher: Executor: BasicTcpResponseDispatcher: send_reply: check 1')
            print('Fetching Socket Context Exception, Error Code is {} and Error Message is: {}'.format(err_message[0], err_message[1]))
            sys.exit()
            
        try:
            socket_context.sendall(req_tcp_res_disp_obj.output_message.message_bytes)
        except socket.error as err_message:
            print('Res Dispatcher: Executor: BasicTcpResponseDispatcher: send_reply: check 2')
            print('Data Sending to client failed, Error Code is {} and Error Message is: {}'.format(err_message[0], err_message[1]))
            sys.exit()
        
        print('Response Sent to Client is Successful')
        
        try:
            socket_context.close()
        except socket.error as err_message:
            print('Res Dispatcher: Executor: BasicTcpResponseDispatcher: send_reply: check 3')
            print('Socket Closing Exception, Error Code is {} and Error Message is: {}'.format(err_message[0], err_message[1]))
            sys.exit()
            
        print('Response Dispatcher Connection Close')