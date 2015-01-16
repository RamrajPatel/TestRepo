import sys
import socket
from globals import GlobalData
from requestparser.communicator import Router
from requestparser.communicator import Request
from requestparser.communicator import InputMessage
from concurrent.futures.thread  import ThreadPoolExecutor
from tcprequestdispatcher.errorhandler import ReqDispatcherException

def process_failure(error_source, error_type, error_msg):
    req_disp_exception_obj = ReqDispatcherException(error_source, error_type, error_msg)
    req_disp_exception_obj.process_exception()
    
class BasicTCPRequestDispatcher(object):
    '''
        Initial class from where Processing will initiate
        Client Request will be accepted here only and
        scheduled to take appropriate Action
    '''
    def dispatch_connection(self, connection):
        print('Dispatching Received Request')
        ''' Receiving Input Request from client '''
        try:
            '''@TODO input request size '''
            input_request_data = connection.recv(10240)
            req_parser_comm_obj = InputMessage('TCP', input_request_data, connection)       
            req_parser_request_obj = Request(req_parser_comm_obj)
            req_parser_router_obj = Router()
            req_parser_router_obj.execute(req_parser_request_obj)
        except socket.error as req_dispatch_error_msg:
            error_source="Executor of TCPRequestDispatcher"
            error_type=req_dispatch_error_msg.__class__.__name__
            error_msg="Problem in Dispatching Connection, Please Contact with Support Team"
            process_failure(error_source, error_type, error_msg)
        except:
            error_source="Executor of TCPRequestDispatcher"
            error_type=sys.exc_info()[0].__name__
            error_msg="Unexpected Error in Dispatching Connection, Please Contact with Support Team"
            process_failure(error_source, error_type, error_msg)
            

if __name__ == '__main__':
    ''' Symbolic name meaning all available interfaces '''
    #HOST_IP = '127.0.0.1'
    ''' Arbitrary non-privileged port  '''
    #REQUEST_PORT = 8802
 
    socketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ('Socket created')
 
    ''' Bind socket to local host and port  '''
    try:
        socketObj.bind((GlobalData.HOST_IP, GlobalData.REQUEST_PORT))
        print ('Socket bind complete')
    except socket.error as bind_fail_err:
        error_source="Executor of TCPRequestDispatcher"
        error_type=bind_fail_err.__class__.__name__
        error_msg="Server Socket Binding Fail"
        #error_code=155
        process_failure(error_source, error_type, error_msg)
    except:
        error_source="Executor of TCPRequestDispatcher"
        error_type=sys.exc_info()[0].__name__
        error_msg="Unexpected Error while Socket Binding"
        #error_code=155
        process_failure(error_source, error_type, error_msg)
        
    '''  Start listening on socket '''
    try:
        socketObj.listen(10)
        print ('Socket is Now listening Mode')
    except socket.error as listen_fail_err:
        error_source="Executor of TCPRequestDispatcher"
        error_type=listen_fail_err.__class__.__name__
        error_msg="Server Socket Listening Problem"
        #error_code=155
        process_failure(error_source, error_type, error_msg)       
    except:
        error_source="Executor of TCPRequestDispatcher"
        error_type=sys.exc_info()[0].__name__
        error_msg="Unexpected Error while Listening"
        #error_code=155
        process_failure(error_source, error_type, error_msg)
    
    tcp_req_obj = BasicTCPRequestDispatcher()
                  
    ''' now keep talking with the client '''
    while True:
        '''    wait to accept a connection - blocking call    '''
        try:
            connection_details, address = socketObj.accept()
            print ('Connected with ' + address[0] + ':' + str(address[1]))
        except socket.error as conn_accept_fail_err:
            error_source="In MAIN of Executor of TCPRequestDispatcher"
            error_type=conn_accept_fail_err.__class__.__name__
            error_msg="Server Socket Connection Accept Problem"
            #error_code=155
            process_failure(error_source, error_type, error_msg)
        except:
            error_source="In MAIN of Executor of TCPRequestDispatcher"
            error_type=sys.exc_info()[0].__name__
            error_msg="Unexpected Error while Accepting Connection"
            #error_code=155
            process_failure(error_source, error_type, error_msg)
        
        ''' 
            start new thread takes 1st argument as a function
            name to be run, second is the tuple of arguments to
            the function.
            _thread.start_new_thread(client thread ,(conn,))
            use Thread pool to service the clients.
        '''
        try:
            with ThreadPoolExecutor(max_workers=3) as executor:
                f1=executor.submit(tcp_req_obj.dispatch_connection(connection_details)) 
        except Exception as thread_pool_fail_msg:
            #print ('Thread  creation Aborted, Return Code is: ' + str(thread_pool_fail_msg[0]) + 'Message is:', thread_pool_fail_msg[1])
            error_source="In MAIN of Executor of TCPRequestDispatcher"
            error_type=thread_pool_fail_msg.__class__.__name__
            error_msg="Thread Creation Aborted, Exiting Program"
            #error_code=155
            process_failure(error_source, error_type, error_msg)
            
    try:        
        socketObj.close()
    except socket.error as socket_close_err:
        error_source="In MAIN of Executor of TCPRequestDispatcher"
        error_type=socket_close_err.__class__.__name__
        error_msg="Server Socket Closing Problem, Exiting Program"
        #error_code=155
        process_failure(error_source, error_type, error_msg)
    except:
        error_source="In MAIN of Executor of TCPRequestDispatcher"
        error_type=sys.exc_info()[0].__name__
        error_msg="Unexpected Error while Closing Connection, Exiting Program"
        #error_code=155
        process_failure(error_source, error_type, error_msg)