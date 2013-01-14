

class Error:

    _error_code = 0
    
    def SetError(self,code):
        Error._error_code = code
       
    def GetLastError(self):
        return Error._error_code