import threading
import time
from Log import logger
class OfflineAntiVirusThread(threading.Thread):
  maxOffAVT = 200000
  idx = 0
  def __init__(self):
    threading.Thread.__init__(self)
    if OfflineAntiVirusThread.idx < OfflineAntiVirusThread.maxOffAVT:
      OfflineAntiVirusThread.idx += 1
    else:
      err = 'Offline AntiVirus resource limited!!!Maximum number %i reached!'
      logger.error(err,OfflineAntiVirusThread.maxOffAVT)

  def run(self,instance_id='instance-0000',offav_config='-r -d max-depth=10 --no-remove'):
    msg = 'OfflineAntiVirus Task %i Started\n'
    task_idx= OfflineAntiVirusThread.idx
    global logger
    logger.debug(msg,task_idx)
    #for i in range(20):
    #while True:
    time.sleep(1234)
    msg = 'OfflineAntiVirus Task %s done\n'
    logger.debug(msg,task_idx)

