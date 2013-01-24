import threading
import tempfile

class F_OffAV:

  def IsImageMountable():
    return True

  def Get_ImagePath(vmid):
    img_path = '/var/lib/nova/instances/%s' %vmid 
    return img_path

  def Get_TmpDir():
    dirname = tempfile.mkdtemp(prefix='oav')
    return dirname

  def Mount_ImageToLocal(img_path,dirname):
    print 'Mount %s to %s\n' %(img_path,dirname)
    return True

  class OffAVTask(threading.Thread):

    maxOffAVT = 2000
    idx = 0

    def __init__(self,dirname,av_args):
      threading.Thread.__init__(self)
      if OffAVTask.idx < OffAVTask.maxOffAVT:
        OffAVTask.idx += 1
      else:
        err = 'Offline AntiVirus resource limited!!!Maximum number %i reached!'
        print err %OffAVTask.maxOffAVT
        #logger.error(err,OffAVTask.maxOffAVT)
