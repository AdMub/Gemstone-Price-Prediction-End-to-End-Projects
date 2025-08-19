# Access to system-related functions
import sys    # used to get details about the error with sys.exc_info()

# creating custom exception class
class customexception(Exception):   # Exception is the parent class of all errors in Python, so your class is like a "special type of error.

    
    # Constructor (__init__)
    def __init__(self, error_message, error_details:sys):
        self.error_message=error_message   # actual error (like "division by zero").
        _,_,exc_tb=error_details.exc_info()  # pass the sys module so you can call sys.exc_info(), it returns; exception type, exception object, traceback object

        self.linemo=exc_tb.tb_lineno  # line number where the error happened.
        self.file_name=exc_tb.tb_frame.f_code.co_filename  # file name of the script where the error occurred.

    
    # __str__ Method
    def __str__(self):  # defines how the error looks when printed
        return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        self.file_name, self.linemo, str(self.error_message))   # prints a human-readable message


# Testing the Exception
if __name__=="__main__":
    try:
        a=1/0   # causes a ZeroDivisionError
    except Exception as e:  # catches the error and stores it in e
        raise customexception(e,sys)   # raises your custom exception instead, passing the original error and system details.