import Handle
import random
from collections import namedtuple

Event = namedtuple('Event', 'time, priority, handle, argument, uid, description')

class E_Base:
    
  _Event_uid = 0
    
  def __init__(self,time,priority,description):
    self.time = time
    self.priority = priority
    self.description = description

  def Gen_Event(self):
    E_Base._Event_uid += 1
    if E_Base._Event_uid > 1000000:
        E_Base._Event_uid = 0
    return Event(self.time,self.priority,self.handle,self.args,E_Base._Event_uid,self.description)  
      
class E_Init(E_Base):
  
  def __init__(self):
    E_Base.__init__(self,time=2,priority=2,description='NORM')
    self.handle = Handle.H_Init().handle
    self.args = ()
  
class E_LoopPerceive(E_Base):

  def __init__(self,time=10,priority=3,description='NORM'):
    E_Base.__init__(self,time,priority,description)
    self.handle = Handle.H_LoopPerceive().handle
    self.args = ()
  
class E_PerceiveVM(E_Base):
    
  def __init__(self,time=6,priority=1,description='NORM'):
      E_Base.__init__(self, time, priority,description)
      self.handle = Handle.H_PerceiveVM().handle
      self.args = ()
        
class E_PerceiveHost(E_Base):

  def __init__(self,time=10,priority=2,description='NORM'):
    E_Base.__init__(self,time,priority,description)
    self.handle = Handle.H_PerceiveHost().handle
    self.args = () 

class E_PerceiveVNet(E_Base):

  def __init__(self,time=8,priority=3,description='NORM'):
    E_Base.__init__(self,time,priority,description)
    self.handle = Handle.H_PerceiveVNet().handle
    self.args = ()

class E_RescueVM(E_Base):

  def __init__(self,args,time=0, priority=1,description='NORM'):
    E_Base.__init__(self,time, priority,description)
    self.handle = Handle.H_RescueVM().handle
    self.args = args

class E_RescueHost(E_Base):

  def __init__(self,args,time=0, priority=1,description='NORM'):
    E_Base.__init__(self,time, priority,description)
    self.handle = Handle.H_RescueHost().handle
    self.args = args

class E_RescueVNet(E_Base):

  def __init__(self,args,time=1, priority=1,description='NORM'):
    E_Base.__init__(self,time, priority,description)
    self.handle = Handle.H_RescueVNet().handle
    self.args = args

class E_Test(E_Base):

  idx = 0
  def __init__(self,args=[],time=60,priority=10,description='TST'):
    E_Base.__init__(self,time,priority,description)
    self.handle = Handle.H_Test().handle
    self.args = args
    E_Test.idx +=1

class E_Worker(E_Base):

  def __init__(self,args=[],time=random.randint(2,20),priority=5,description='TST'):
    E_Base.__init__(self,time,priority,description)
    self.handle = Handle.H_Worker().handle
    self.args = args

class E_StartOffAV(E_Base):

  def __init__(self,args=[],time=3,priority=5,description='NORM'):
    E_Base.__init__(self,time,priority,description)
    self.handle = Handle.H_StartOffAV().handle
    self.args = args

class E_StopOffAV(E_Base):

  def __init__(self,args=[],time=3,priority=5,description='NORM'):
    E_Base.__init__(self,time,priority,description)
    self.handle = Handle.H_StopOffAV().handle
    self.args = args
