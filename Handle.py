from Execution.error import Error
from Execution.Instance import F_Instance
import whu_sched
import time
import Event
from Execution.Volume import F_Volume
from Perceive.VM import F_VMStatus
import random

class Handler(Error):
    pass

class H_Init(Handler):
    
    def handle(self):
        scheduler = whu_sched.scheduler(time.time,time.sleep)
	print 'scheduler initialized\n'
        E = Event.E_LoopPerceive()
        event = E.Gen_Event()
        scheduler.enter(*event)
	print 'Initial event added\n'

class H_RescueVM(Handler):
    
    def handle(self,instance_id = 'instance-00000000'):
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

class H_PerceiveVM(Handler):
    
    def handle(self):
	print 'F_VMStatus called\n'
	print 'F_GetVMStatus called\n'
	rnd = random.randint(0,99)
	if rnd >40 and rnd < 45:
	  print 'VM status anomaly detected\n'
	  scheduler = whu_sched.scheduler(time.time,time.sleep)
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
	print 'H_PerceiveVM handled\n'
        #VM = F_VMStatus
        #VM.F_GetVMStatus()
class H_LoopPerceive(Handler):
    def handle(self):
	scheduler = whu_sched.scheduler(time.time,time.sleep)
        E = Event.E_PerceiveVM()
        event = E.Gen_Event()
        scheduler.enter(*event)
#	E = Event.E_LoopPerceive()
#	event = E.Gen_Event()
#	scheduler.enter(*event)
	print 'LoopPerceive handled\n'
