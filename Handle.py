from Execution.error import Error
from Execution.Instance import F_Instance
import whu_sched
import time
import Event
from Execution.Volume import F_Volume
from Perceive.VM import F_VMStatus
import random

import logging
logger = logging.getLogger('whu_sched')
hdlr = logging.FileHandler('/var/tmp/whu_sched.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

#global scheduler
#scheduler = whu_sched.scheduler(time.time,time.sleep)

class Handler(Error):
    pass

class H_Init(Handler):
    
    def handle(self):
	global logger
#	global scheduler
        scheduler = whu_sched.scheduler(time.time,time.sleep)
	msg = 'scheduler initialized'
	logger.debug(msg)
	print msg
        E = Event.E_LoopPerceive()
        event = E.Gen_Event()
        scheduler.enter(*event)
	msg = 'Initial event %s added'
	logger.debug(msg,event[4])
	print msg %event[4]
	
	E = Event.E_Test()
	event = E.Gen_Event()
	scheduler.enter(*event)
	
	msg = '\n\n\n\n\n\n\nTest event id is %s \n\n\n\n\n\n\n\n\n\n'
	logger.debug(msg,event[4])
	print msg %event[4]
 
	#time.sleep(3)

class H_LoopPerceive(Handler):
    def handle(self):
	global logger
	#global scheduler
	scheduler = whu_sched.scheduler(time.time,time.sleep)
	#Enter PerceiveVM event
        E = Event.E_PerceiveVM()
        event = E.Gen_Event()
        scheduler.enter(*event)
	#Enter PerceiveHost event
        E = Event.E_PerceiveHost()
        event = E.Gen_Event()
        scheduler.enter(*event)
	#Enter PerceiveVNet event
        E = Event.E_PerceiveVNet()
        event = E.Gen_Event()
        scheduler.enter(*event)
	#Enter LoopPerceive again
	E = Event.E_LoopPerceive()
	event = E.Gen_Event()
	scheduler.enter(*event)
	msg = "size of queue is %s"
	logger.debug(msg,len(scheduler._queue))
	print msg %len(scheduler._queue)
	msg = 'LoopPerceive handled'
	logger.debug(msg)
	#print msg
#	i =0
#	while i<len(scheduler._queue):	
#	  print scheduler._queue[i]
#	  i +=1
#	time.sleep(5)

class H_PerceiveVM(Handler):
    
    def handle(self):
	global logger
#	print 'F_VMStatus called\n'
#	print 'F_GetVMStatus called\n'
	rnd = random.randint(0,99)
	#global scheduler
	scheduler = whu_sched.scheduler(time.time,time.sleep)
	if rnd >40 and rnd < 50:
	  msg = "VM %s status anomaly detected"
	  vmname = random.choice(['instance-00000001','instance-00000002','instance-00000003','instance-00000004',])
	  logger.warn(msg,vmname)
	  print msg %vmname
	  args=[]
	  args.append(vmname)
	  #print 'args for E_RescueVM is ',args
          E = Event.E_RescueVM(args)
          event = E.Gen_Event()
          scheduler.enter(*event)
	  msg = 'RescueVM event %s added'
	  logger.debug(msg,event[4])
	  print msg %event[4]
	else:
	  msg = "VM status is Ok,size of queue is %s"
	  logger.debug(msg,len(scheduler._queue))
	  print msg %len(scheduler._queue)
	msg = 'H_PerceiveVM handled'
	logger.debug(msg)
	print msg
        #VM = F_VMStatus
        #VM.F_GetVMStatus()

class H_PerceiveHost(Handler):
  def handle(self,host_id = 'host-0000'):
    global logger
#    print 'F_HostStatus called\n'
#    print 'F_GetHostStatus called\n'
    rnd = random.randint(0,99)
    #global scheduler
    scheduler = whu_sched.scheduler(time.time,time.sleep)
    if rnd >40 and rnd < 45:
      msg = "Host %s status anomaly detected"
      hostname = random.choice(['host-0001','host-0002','host-0003','host-0004',])
      logger.warn(msg,hostname)
      print msg %hostname
      args=[]
      args.append(hostname)
      #print 'args for E_RescueVM is ',args
      E = Event.E_RescueHost(args)
      event = E.Gen_Event()
      scheduler.enter(*event)
      msg = 'RescueHost event %s added'
      logger.debug(msg,event[4])
      print msg %event[4]
    else:
      msg = 'Host status is Ok ,size of queue is %s'
      logger.debug(msg,len(scheduler._queue))
      print msg %len(scheduler._queue)
    msg = 'H_PerceiveHost handled'
    logger.debug(msg)
    print msg

class H_PerceiveVNet(Handler):
  def handle(self):
    global logger
    msg = "PerceiveVNet handled"
    logger.debug(msg)
    print msg

class H_RescueVM(Handler):
    def handle(self,instance_id = 'instance-00000000'):
	global logger
	msg = "H_RescueVM handled with %s"
	logger.debug(msg,instance_id)
	print msg %instance_id
        #instance = F_Instance()
        #instance_name = instance.Get_SpecificInstanceName(instance_id)
        #image_id = instance.Get_InstanceImageId(instance_id)
        #flavor_id = instance.Get_InstanceFlavorId(instance_id)
        #new_instance_details = instance.Create_Instance(instance_name, image_id, flavor_id)
        #new_instance_id = new_instance_details['server']['id']
        #while True:
        #    if VM[instance_name]['status']=='ACTIVE':
        #        volume = F_Volume()
        #        volume.Attach_VolumeToInstance(new_instance_id)
        #        break

class H_RescueHost(Handler):
  def handle(self,host_id = 'host-0000'):
    global logger
    msg = 'H_RescueHost handled with %s'
    logger.debug(msg,host_id)
    print msg %host_id

class H_RescueVNet(Handler):
  def handle(self):
    global logger
    msg = 'H_RescueVNet handled'
    logger.debug(msg)
    print msg
    

#for test
class H_Test(Handler):
  def handle(self):
    msg = 'Hello test ',Event.E_Test.idx
    logger.debug(msg)
    print msg
