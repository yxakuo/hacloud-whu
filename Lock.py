class Wakeup_Lock:

    _lock = False
    
    def OpenLock(self):
        Wakeup_Lock._lock = True
        
    def CloseLock(self):
        Wakeup_Lock._lock = False
        
    def IsLocked(self):
        return not Wakeup_Lock._lock