import threading
import tempfile

class F_OffAV:

  def IsImageMountable(self):
    return True

  def Get_ImagePath(self,vmid):
    base_path_opt ='/var/lib/nova/instances/'#get from cfg later 
    img_path =  base_path_opt+vmid 
    return img_path

  def Get_TmpDir(self):
    prefix_opt = 'oav'#get from cfg later
    dirname = tempfile.mkdtemp(prefix=prefix_opt)
    return dirname

  def Mount_ImageToLocal(self,img_path,dirname):
    print 'Mount %s to %s\n' %(img_path,dirname)
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

  def ClamAVFunc(self,domethod,targetdir):
    print 'Running in Clamav thread with options %s scanning %s\n' %(domethod,targetdir)
    pass

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
    def __init__(self,dirname,av_args):
      threading.Thread.__init__(self,target = F_OffAV().Get_AVFunc(av_args['avSoft']), args = (av_args['doMethod'],dirname+av_args['scanDir']))
      if F_OffAV.OffAVTask.idx < F_OffAV.OffAVTask.maxOffAVT:
        F_OffAV.OffAVTask.idx += 1
      else:
        err = 'Offline AntiVirus resource limited!!!Maximum number %i reached!'
        print err %F_OffAV.OffAVTask.maxOffAVT
        #logger.error(err,OffAVTask.maxOffAVT)
