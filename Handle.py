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

class Handler(Error):
    pass

class H_Init(Handler):
    
    def handle(self):
	global logger
	logger.info(time.time())
        scheduler = whu_sched.scheduler(time.time,time.sleep)
	print 'scheduler initialized\n'
        E = Event.E_LoopPerceive()
        event = E.Gen_Event()
        scheduler.enter(*event)
	print 'Initial event added\n'

class H_LoopPerceive(Handler):
    def handle(self):
	global logger
	logger.info(time.time())
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
	print 'size of queue is ',len(scheduler._queue)
	print 'LoopPerceive handled\n'

class H_PerceiveVM(Handler):
    
    def handle(self):
	global logger
	logger.info(time.time())
	print 'F_VMStatus called\n'
	print 'F_GetVMStatus called\n'
	rnd = random.randint(0,99)
	scheduler = whu_sched.scheduler(time.time,time.sleep)
	if rnd >40 and rnd < 50:
	  print 'VM status anomaly detected\n'
	  vmname = random.choice(['instance-00000001','instance-00000002','instance-00000003','instance-00000004',])
	  print 'anomaly occurred in ',vmname,'\n'
	  args=[]
	  args.append(vmname)
	  #print 'args for E_RescueVM is ',args
          E = Event.E_RescueVM(args)
          event = E.Gen_Event()
          scheduler.enter(*event)
	  print 'RescueVM event added\n'
	else:
	  print 'VM status is Ok\n'
	  print 'size of queue is ',len(scheduler._queue)
	print 'H_PerceiveVM handled\n'
        #VM = F_VMStatus
        #VM.F_GetVMStatus()

class H_PerceiveHost(Handler):
  def handle(self,host_id = 'host-0000'):
    global logger
    logger.info(time.time())
    print 'F_HostStatus called\n'
    print 'F_GetHostStatus called\n'
    rnd = random.randint(0,99)
    scheduler = whu_sched.scheduler(time.time,time.sleep)
    if rnd >40 and rnd < 45:
      print 'Host status anomaly detected\n'
      hostname = random.choice(['host-0001','host-0002','host-0003','host-0004',])
      print 'anomaly occurred in ',hostname,'\n'
      args=[]
      args.append(hostname)
      #print 'args for E_RescueVM is ',args
      E = Event.E_RescueHost(args)
      event = E.Gen_Event()
      scheduler.enter(*event)
      print 'RescueHost event added\n'
    else:
      print 'Host status is Ok\n'
      print 'size of queue is ',len(scheduler._queue)
    print 'H_PerceiveHost handled\n'

class H_PerceiveVNet(Handler):
  def handle(self):
    global logger
    logger.info(time.time())
    print 'PerceiveVNet handled\n'
class H_RescueVM(Handler):
    def handle(self,instance_id = 'instance-00000000'):
	global logger
	logger.info(time.time())
	print 'F_instance called\n'
	print instance_id,' is rescued\n'
	print 'H_RescueVM handled\n'
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
    logger.info(time.time())
    print 'H_RescueHost handled\n'

class H_RescueVNet(Handler):
  def handle(self):
    global logger
    logger.info(time.time())
    print 'H_RescueVNet handled\n'
