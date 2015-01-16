import sys
class A(object):
    def __init__(self):
        print('Inside init Constructor')

class B(object):
    def __init__(self):
        self.process()
        
    def process(self):
        print(A().__module__)
                
if __name__ == '__main__':
    print(type(A()))
    print(A().__class__.__name__)
    B()
    print(A().__class__.__module__)
    
    try:
        a=2/0
    except IOError as e:
        pass
    except:
        print('unexpected error', sys.exc_info()[0].__name__)
    
    try:
        a=2/0
    except IOError as e:
        pass
    except ZeroDivisionError as err:
        print(err.__class__.__name__)