class Request(object):
	pass
	
class Response(object):
	#pass
	error_response=None
	
	def __init__(self):
		print('TCP Request Dispatcher Response Created')
		
	def set_response(self, error_response):
		self.error_response = error_response
		
	def handle_exception(self):
		print('Error Code:' + str(self.error_response[0]) + 'Error Message: ' + self.error_response[1])
			
class Router(object):
	pass
	
	