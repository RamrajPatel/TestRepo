from responseparser.executor import  BasicResponseParser

'''
Created on 14-Aug-2014

@author: Ashim
'''

class Request:
    '''
        Response Parser Request Class
    '''
    ''' 
        This is the Session object which Service
        gives in its response
    '''
    new_session=None
    status=None
    
    def __init__(self, new_session, status):
        '''
            Constructor
        '''
        self.new_session=new_session
        self.status=status
        

class Router(object):
    '''
        Router Class of Response Parser Communicator Module
    '''
    def __init__(self):
        '''
            Constructor
        '''
    
    def execute(self, req_res_parser_obj):
        print('exec Router Response parser')
        resp_parser_exec_obj = BasicResponseParser()
        resp_parser_exec_obj.parse(req_res_parser_obj)


class Response(object):
    pass