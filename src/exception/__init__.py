# importing libraries
import os
import sys


class CustomException(Exception):
    # creating init function for error_message and error_details
    def __init__(self, error_message: Exception, error_details: sys):
        # creating super class for calling error_message
        super().__init__(error_message)
        self.error_message = CustomException.get_detailed_error_message(
            error_message=error_message, error_details=error_details)

    @staticmethod
    # defining error_message_detail function
    def get_detailed_error_message(error_message: Exception, error_details: sys) -> str:
        # execution traceback - error details and execution details
        _, _, exec_tb = error_details.exc_info()
        # execution traceback in exception block frame by frame and line by line
        exception_block_line_number = exec_tb.tb_frame.f_lineno
        # execution traceback in try block through line by line
        try_block_line_number = exec_tb.tb_lineno
        # execution traceback in file name frame by frame file by file and code by code
        file_name = exec_tb.tb_frame.f_code.co_filename
        # getting the entire error message
        error_message = f"""
        Error occurred in execution of :
        [{file_name}] at 
        try block line number : [{try_block_line_number}]
        and exception block line number : [{exception_block_line_number}]
        error message [{error_message}]
        """

        return error_message

    def __str__(self):
        return self.error_message

    def __repr__(self):
        return CustomException.__name__.__str__()
