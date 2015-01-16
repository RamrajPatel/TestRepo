'''
    Created on 14-Aug-2014
    @author: Ashim
'''

import sys
from utilitymodule import loadparamfile
from tcpresponsedispatcher.communicator import Router
from tcpresponsedispatcher.communicator import Request
from tcpresponsedispatcher.communicator import OutputMessage

outputDictString={"comm_msg": {}}

class Encoder(object):
    '''
        This class will convert Output Python Object into JSON Response
    '''
    
    encode_output_message=None
    
    def __init__(self):
        print('Inside Encoder Class')
        
    def encode_pyobject(self, response_message):
        encode_output_message = loadparamfile.json.dumps(response_message, default=lambda o: o.__dict__, indent=4, sort_keys=True)
        print(encode_output_message)
        return encode_output_message


class BasicResponseParser(object):
    def __init__(self):
        print('In BasicResponseParser Constructor')
    
    def get_error_params_file_name(self):
        return loadparamfile.GlobalData.ERROR_PARAMS_FNAME
    
    def get_error_details(self, error_type, ref_erm_param):
        error_exit_flag=True
        error_description="Hello"
        error_code=1001
        return error_code, error_description, error_exit_flag
    
    def process_error(self, req_res_parser_obj):
        print('Inside process_error in Response Parser')
        '''
            Load Error Parameters
        '''
        try:
            erm_param_file=self.get_error_params_file_name()
            ref_erm_param=loadparamfile.LoadParamsFile(erm_param_file)
        except:
            print('hello')
        print(ref_erm_param)
        
        print('Error Message: {}'.format(req_res_parser_obj.new_session.error_msg))
        print('Error Type: {}'.format(req_res_parser_obj.new_session.error_type))
        print('Error Source: {}'.format(req_res_parser_obj.new_session.error_source))
        
        error_type = req_res_parser_obj.new_session.error_type
        '''
            Get Error Details
        '''
        error_code, error_description, error_exit_flag = self.get_error_details(error_type, ref_erm_param)
        
        print('Error Code: ', error_code)
        print('Error Description: ', error_description)
        print('Error Exit Flag: ', error_exit_flag)
        
        '''
            If Error can not be sent to Front-End Server then do Exit here
            Otherwise Generate Response for Output Data
            Also load ERMPARAM file to load error codes and other details
        '''
        if error_exit_flag == "EXIT":
            print('Encountered System Error, Exiting Program, Error Code: {} and Error Description : {}', error_code, error_description)
            sys.exit()
        else:
            '''
                Preparing Error Response For Given Request
            '''
            print('Generating Error Response')
            outputDictString["comm_msg"]["response_stat"] = "ERROR"
            outputDictString["comm_msg"]["error_info"]["error_code"] = error_code
            if req_res_parser_obj.new_session.error_msg and not req_res_parser_obj.new_session.error_msg.isspace():
                outputDictString["comm_msg"]["error_info"]["error_msg"] = req_res_parser_obj.new_session.error_msg
            else:
                outputDictString["comm_msg"]["error_info"]["error_msg"] = error_description
            outputDictString["comm_msg"]["error_info"]["error_type"] = req_res_parser_obj.new_session.error_type
            outputDictString["comm_msg"]["error_info"]["error_source"] = req_res_parser_obj.new_session.error_source
            return outputDictString
            
    def parse(self, req_res_parser_obj):
        print('In Parse method of BasicResponseParser Class')
        if req_res_parser_obj.status == "ERROR":
            response_message = self.process_error(req_res_parser_obj)
        else:
            response_message = req_res_parser_obj.new_session.session.message.message_data
            message_id = req_res_parser_obj.new_session.session.message.message_id
            print('Message Id: ', message_id)
    
        ''' Fetching Socket Context From Globally Maintained List ''' 
        #SocketContext = loadparamfile.GlobalData.store_socket[1]
        SocketContext = loadparamfile.GlobalData.store_socket[message_id]
    
        ''' Prepare your Response Object and Pass it to the 
            given below mention Object
            for time being it is Decoded Request Object
        '''
        print('Encoding JSON String into Request Parser')
        encoded_output_message = Encoder().encode_pyobject(response_message)
        print(encoded_output_message)
        
        ''' Encoding Back the Message in Bytes '''
        message_bytes = bytes(encoded_output_message, 'UTF-8')
        
        output_message = OutputMessage(SocketContext, message_bytes)      
        req_tcp_res_disp_obj = Request(output_message)
        router_tcp_res_disp_obj = Router()
        router_tcp_res_disp_obj.execute(req_tcp_res_disp_obj)