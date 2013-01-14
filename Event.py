import Handle
from collections import namedtuple

Event = namedtuple('Event', 'time, priority, handle, argument, uid')

class E_Base:
    
    _Event_uid = 0
    
    def __init__(self,time,priority):
        self.time = time
        self.priority = priority
        

    def Gen_Event(self):
        E_Base._Event_uid = E_Base._Event_uid + 1
        if E_Base._Event_uid > 65535:
            E_Base._Event_uid = 0
        return Event(self.time,self.priority,self.handle,self.args,E_Base._Event_uid)  
      
class E_Init(E_Base):
    
    def __init__(self):
	E_Base.__init__(self,time=2,priority=2)
        self.handle = Handle.H_Init().handle
        self.args = ()
    
    
class E_RescueVM(E_Base):
    
    def __init__(self,args,time=0, priority=1):
        E_Base.__init__(self,time, priority)
        self.handle = Handle.H_RescueVM().handle
        self.args = args
class E_PerceiveVM(E_Base):
    
    def __init__(self,time=6,priority=1):
        E_Base.__init__(self, time, priority)
        self.handle = Handle.H_PerceiveVM().handle
        self.args = ()
        
class E_LoopPerceive(E_Base):
    def __init__(self,time=6,priority=3):
	E_Base.__init__(self,time,priority)
	self.handle = Handle.H_LoopPerceive().handle
	self.args = ()
