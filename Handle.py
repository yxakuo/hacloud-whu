import whu_sched
import time
import Event
import random
from Log import logger 
from OfflineAntiVirus import OfflineAntiVirusThread
#from Execution.Volume import F_Volume
#from Perceive.VM import F_VMStatus
from Execution.error import Error
#from Execution.Instance import F_Instance
import sys
import tempfile
from offav import F_OffAV

class VM_Profile:
  def __init__(self,vmid='instance-00000000',userid='user-0000',hostid='host-0000'):
    self.vmid = vmid
    self.userid = userid
    self.hostid = hostid

class Handler(Error):
  pass

class H_Init(Handler):
    
  def handle(self):
    global logger
    scheduler = whu_sched.scheduler(time.time,time.sleep)
    msg = 'scheduler initialized'
    logger.debug(msg)
    #print msg
    E = Event.E_LoopPerceive()
    event = E.Gen_Event()
    scheduler.enter(*event)
    msg = 'Initial event %s added'
    logger.debug(msg,event[4])
    #print msg %event[4]
#for test    
#    E = Event.E_Test()
#    event = E.Gen_Event()
#    scheduler.enter(*event)
#    
#    msg = '!********Test event id is %s********!'
#    logger.debug(msg,event[4])
#    print msg %event[4]

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

    msg = "LoopPerceive handled,size of queue is %s"
    logger.debug(msg,len(scheduler._queue))
    #print msg %len(scheduler._queue)
    # scheduler.print_queue()
    #	time.sleep(5)

class H_PerceiveVM(Handler):
    
  def handle(self):
    global logger
    rnd = random.randint(0,99)
    #global scheduler
    scheduler = whu_sched.scheduler(time.time,time.sleep)
    if rnd >40 and rnd < 50:
      msg = "VM %s status anomaly detected"
      vmname = random.choice(['instance-00000001','instance-00000002','instance-00000003','instance-00000004',])
      logger.warn(msg,vmname)
      #print msg %vmname
      args=[]
      args.append(vmname)
      #print 'args for E_RescueVM is ',args
      E = Event.E_RescueVM(args)
      event = E.Gen_Event()
      scheduler.enter(*event)
      msg = 'RescueVM event %s added'
      logger.debug(msg,event[4])
      #print msg %event[4]
    else:
      msg = "VM status is Ok,size of queue is %s"
      logger.debug(msg,len(scheduler._queue))
      #print msg %len(scheduler._queue)
    msg = 'H_PerceiveVM handled'
    logger.debug(msg)
    #print msg
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
      #print msg %hostname
      args=[]
      args.append(hostname)
      #print 'args for E_RescueVM is ',args
      E = Event.E_RescueHost(args)
      event = E.Gen_Event()
      scheduler.enter(*event)
      msg = 'RescueHost event %s added'
      logger.debug(msg,event[4])
      #print msg %event[4]
    else:
      msg = 'Host status is Ok ,size of queue is %s'
      logger.debug(msg,len(scheduler._queue))
      #print msg %len(scheduler._queue)
    msg = 'H_PerceiveHost handled'
    logger.debug(msg)
    #print msg

class H_PerceiveVNet(Handler):

  def handle(self):
    global logger
    msg = "PerceiveVNet handled"
    logger.debug(msg)
    #print msg

class H_RescueVM(Handler):

  def handle(self,instance_id = 'instance-00000000'):
    global logger
    msg = "H_RescueVM handled with %s"
    logger.debug(msg,instance_id)
    #print msg %instance_id
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
    #print msg %host_id

class H_RescueVNet(Handler):

  def handle(self):
    global logger
    msg = 'H_RescueVNet handled'
    logger.debug(msg)
    print msg
    

#for test
class H_Test(Handler):

  def handle(self):
    msg = '$$$$$$====== Hello test %i =====$$$$$$ '
    logger.debug(msg,Event.E_Test.idx)
    print msg %Event.E_Test.idx

class H_Worker(Handler):

  def handle(self):
    msg = '@@@@@@====== Worker test ======@@@@@@ '
    logger.debug(msg)
    print msg
#    i = random.randint(0,99)
#    if i>5 and i <70:
#      event = Event.E_Worker().Gen_Event()
#      scheduler = whu_sched.scheduler(time.time,time.sleep)
#      scheduler.enter(*event)
#      msg = 'New E_Worker event entered!\n'
#      logger.debug(msg)
#      print msg
#    time.sleep(3)
    t = OfflineAntiVirusThread()
    t.setDaemon(True)
    t.start()
    print 'An OffAVT started\n'
    msg = '/********** Worker Handled ***********/\n'
    logger.debug(msg)
    print msg

class H_StartOffAV(Handler):

  def handle(self,vm_profiles=[],av_args={'avSoft':'$DEFAULT_AVSOFT','doMethod':'$DEFAULT_DO_METHOD','scanDir':'$HOME'}):
    msg = 'In StartOffAV handle\n'
    print msg
    if not len(vm_profiles):
      print 'All virtual machines would start OffAV Tasks.\n'
      all_vms = [VM_Profile('instance-00000001','user-0002','host-0003'),VM_Profile('instance-00000002','user-0002','host-0002'),VM_Profile('instance-00000003','user-0001','host-0001'),VM_Profile('instance-00000004','user-0003','host-0002')]
      vm_profiles = all_vms

    for vm in vm_profiles:
      vmid = vm.vmid
      userid = vm.userid
      hostid = vm.hostid
      if not True: #F_OffAV.IsImageMountable(vmid,userid,hostid):
        #raise VMImageUnmountableError
        print 'The image of  %s is unmountable!' %vmid
        continue
      print 'The image of %s is mountable. ' %vmid
      #get image path
      img_path = F_OffAV.Get_ImagePath(vmid,userid,hostid)
      if img_path is None:
        #raise VMImageMissingError
        print 'Fail to get the image of %s %s %s!' %(vmid,userid,hostid)
        continue
      print 'The image path of %s is %s.' %(vmid,img_path)
      #create tmp directory for mounting the image
      dirname = F_OffAV.Get_TmpDir()
      if dirname is None:
        print 'Unable to create temp directory for image mounting!'
        #raise MkdTempError
        continue
      #mount the vm image to tmp directory
      r = F_OffAV.Mount_ImageToLocal(img_path,dirname)
      #set up a worker thread to scan the mounted image
      if r:
        print 'VM image has been mounted to local temp dir.\n'
        t = F_OffAV.OffAVTask(dirname,av_args)
        t.setDaemon(True)
        #TODO:append t to global daemon threads list for further control over them
        t.start()
      else:
        print 'Fail to mount the VM image to local temp dir.\n'
        #raise MountLocalError
        continue
#default arguments override by the passed-ins
