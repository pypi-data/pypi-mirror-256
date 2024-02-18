'''
utils.cmd_executor
===================

This module contains the static class responsible for executing bash commands and returning the output and error. 
'''

import subprocess

class BashExecutor:
    ''' A static class to execute bash commands and return the output and error as a tuple.'''
    
    @staticmethod
    def execute_cmd(_cmd):
        _p = subprocess.Popen(_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        
        # returns (output, error) tuple
        return _p.communicate()
        

if __name__ == '__main__':
    b = BashExecutor()
