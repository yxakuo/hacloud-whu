import threading
import tempfile
import guestfs

class F_OffAV:

  def IsImageMountable(self):
    #check the global table of vm_state whether the vm is running or shutdown or destroyed.
    return True

  def Get_ImagePath(self,vmid):
    base_path_opt ='/var/lib/nova/instances/'#get from cfg later 
    img_path =  base_path_opt+vmid 
    return '/home/me/workshopSuse/home/me/winXP_1.5G'

  def Get_TmpDir(self):
    prefix_opt = 'oav'#get from cfg later
    dirname = tempfile.mkdtemp(prefix=prefix_opt)
    return dirname

  def Mount_ImageToLocal(self,img_path,dirname):
    print 'Mount %s to %s\n' %(img_path,dirname)
    g = guestfs.GuestFS()
    #stat whether the image exists
    g.add_drive_opts(img_path,"raw")
    g.launch()
    partitions = g.list_partitions()
    if len(partitions) == 0:
      print 'No partition found in the image!\n'
      #raise NoPartitionImageError
      return False

    for p in partitions:
      i = 0 
      #the temp directory with dirname ,for each partition
      pdirname = tempfile.mkdtemp(prefix=str(i))
      i += 1
      options = ["user_xattr",p,"/"]
      g.mount_local(pdirname,)

    return True

  def Get_AVFunc(self,avsoftname):
    if avsoftname.lower() == 'clamav':
      return self.ClamAVFunc
    elif avsoftname.lower() in ['avast','biubiu']:
      return self.DefaultAVFunc
    else:
      print 'The antivirus %s can not be found,make sure it`s installed.\n' %avsoftname
      #raise NoAVSoftError
      return None

  def ClamAVFunc(self,vm,av_args):
    print 'Running in Clamav thread scanning %s\n' %(vm.vmid)
    img_path = self.Get_ImagePath(vm.vmid)
    dirname = self.Get_TmpDir()

    g = guestfs.GuestFS()
    g.add_drive_opts(img_path,format="raw")
    g.launch()
    partitions = g.list_partitions()
    if len(partitions) == 0:
      print 'No partition found in the image!\n'
      #raise NoPartitionImageError
      return False

    for p in partitions:
      #TODO:Check the opts
      #mount_options(self, options, device, mountpoint)
      g.mount_options("user_xattr",p,"/")
      g.mount_local(dirname)
      #Bug:infinite loop?
      if g.mount_local_run() == -1:
        print 'Fail to mount local!\n'
        #raise MountLocalError
        continue
      print 'Scanning partition %s .......\n' %p
      print 'Finish scanning partition %s .......\n' %p
      g.umount_local()

    g.umount("/")
    g.close()
    print 'Finished!\n'

  def DefaultAVFunc(domethod,targetdir):
    print 'Running in Default thread with options %s scanning %s\n' %(domethod,targetdir)
    pass

  class OffAVTask(threading.Thread):

    maxOffAVT = 2000#get from cfg later
    idx = 0

    #dirname: local directory the image mounted to,the final directory for scanning is dirname concated with av_args['scanDir']
    #av_args: avSoft,the antivirus soft to be used;
    #         doMethod,the functional options for antivirus;
    #         scanDir,the directory to be scanned within virtual machine
    def __init__(self,vm,av_args):
      threading.Thread.__init__(self,target = F_OffAV().Get_AVFunc(av_args['avSoft']), args = (vm,av_args))
      if F_OffAV.OffAVTask.idx < F_OffAV.OffAVTask.maxOffAVT:
        F_OffAV.OffAVTask.idx += 1
      else:
        err = 'Offline AntiVirus resource limited!!!Maximum number %i reached!'
        print err %F_OffAV.OffAVTask.maxOffAVT
        #logger.error(err,OffAVTask.maxOffAVT)
